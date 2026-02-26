# Distributed Inference Exploration -- Design

**Date:** 2026-02-24
**Goal:** Run 30B+ LLM inference across titan-pi + titan-pc using three frameworks, compare results, then design a soul-mesh native hybrid.

## Hardware

| Node | CPU | Arch | RAM | Storage | Role |
|------|-----|------|-----|---------|------|
| titan-pi | 4-core ARM | aarch64 | 16 GB | ~60 GB | Hub, main node |
| titan-pc | i5-8400 6-core | x86_64 | 7.6 GB | 3.7 TB | Agent, worker |

- No discrete GPU on either node (titan-pc has UHD 630 iGPU, negligible)
- LAN connection between nodes
- Combined RAM: ~23.6 GB

## Test Models

| Model | Type | Params | Quant | Size (est.) | Why |
|-------|------|--------|-------|-------------|-----|
| Qwen3-30B-A3B | MoE | 30B total, 3B active | Q4_K_M | ~18 GB | Sparse -- tests layer distribution with low active compute |
| DeepSeek-R1-Distill-Qwen-32B | Dense | 32B | Q4_K_M | ~19 GB | Dense -- true test of distributed compute across all params |

## Standard Test Protocol

Each framework runs the same test so results are directly comparable.

### Prompt

```
System: You are a technical writer. Be concise and precise.
User: Explain how distributed systems achieve consensus in exactly 3 paragraphs.
```

~100 tokens input, expect ~200-300 tokens output.

### Metrics

| Metric | How to capture |
|--------|---------------|
| Time to first token (TTFT) | Timestamp delta from request to first streamed token |
| Tokens/second (generation) | Total tokens / generation time |
| Peak RAM per node | Monitor with `/proc/meminfo` before, during, after |
| Network transfer | `ifstat` or `nethogs` during inference |
| Model load time | Time from process start to "ready" |
| Success/Failure | Binary -- did it produce coherent output? |

### Environment Setup (common)

1. Download both GGUF models to titan-pi (`~/models/`)
2. Copy models to titan-pc as needed (`scp` or shared NFS)
3. Ensure both nodes can reach each other (ping, port checks)
4. Kill other heavy processes during benchmarks
5. Run each test 3 times, take median

---

## Phase 1: llama.cpp RPC

**Source:** https://github.com/ggml-org/llama.cpp

### What it does

Main node runs `llama-server` with model loaded. Worker nodes run `rpc-server` exposing CPU compute. Main node distributes layers to workers proportional to available memory. All tensor operations executed remotely on workers.

### Setup steps

1. **Build on titan-pi (aarch64):**
   ```bash
   git clone https://github.com/ggml-org/llama.cpp
   cd llama.cpp
   mkdir build && cd build
   cmake .. -DGGML_RPC=ON
   cmake --build . --config Release -j4
   ```

2. **Build on titan-pc (x86_64):**
   ```bash
   # Same steps, x86 will pick up AVX2 automatically
   git clone https://github.com/ggml-org/llama.cpp
   cd llama.cpp
   mkdir build && cd build
   cmake .. -DGGML_RPC=ON
   cmake --build . --config Release -j6
   ```

3. **Start RPC worker on titan-pc:**
   ```bash
   ./build/bin/rpc-server -p 50052
   ```

4. **Start main node on titan-pi:**
   ```bash
   ./build/bin/llama-server \
     -m ~/models/Qwen3-30B-A3B-Q4_K_M.gguf \
     --rpc titan-pc:50052 \
     --host 0.0.0.0 --port 8080 \
     -t 4 -c 2048
   ```

5. **Run inference:**
   ```bash
   curl http://localhost:8080/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d '{"model":"qwen","messages":[{"role":"system","content":"You are a technical writer. Be concise and precise."},{"role":"user","content":"Explain how distributed systems achieve consensus in exactly 3 paragraphs."}],"stream":true}'
   ```

6. Repeat with DeepSeek-R1-Distill-Qwen-32B model.

### Key questions to answer

- Does mixed aarch64 + x86_64 RPC work at all?
- How does llama.cpp split layers between nodes (auto by RAM)?
- What's the network overhead for tensor operations?
- How does `--tensor-split` manual override compare to auto?

### Risk

ARM CPU-only RPC has reported issues (GitHub #11807). May need to run main node on titan-pc (x86) instead if ARM RPC fails.

---

## Phase 2: exo

**Source:** https://github.com/exo-explore/exo

### What it does

Peer-to-peer pipeline parallelism. Splits model into contiguous layer shards, each device runs its shard. Auto-discovers peers. Uses tinygrad backend on Linux.

### Setup steps

1. **Install on both nodes:**
   ```bash
   pip install exo
   # or: git clone + pip install -e .
   ```

2. **Configure CPU backend (no GPU):**
   ```bash
   export CLANG=1  # Forces tinygrad to use CPU via clang
   ```

3. **Start exo on titan-pi:**
   ```bash
   exo run
   ```

4. **Start exo on titan-pc:**
   ```bash
   exo run
   ```
   (Auto-discovery should find each other on LAN)

5. **Run inference via exo's API:**
   ```bash
   curl http://localhost:52415/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d '{"model":"qwen3-30b-a3b","messages":[...],"stream":true}'
   ```

6. Repeat with DeepSeek model.

### Key questions to answer

- Does tinygrad CPU backend (CLANG=1) work on both aarch64 and x86_64?
- How does exo partition layers across heterogeneous nodes?
- Performance comparison: tinygrad CPU vs llama.cpp CPU
- Does auto-discovery work reliably on our LAN?
- How does exo handle model download/distribution?

### Risk

tinygrad CPU performance may be significantly worse than llama.cpp. exo is primarily optimized for Apple Silicon MLX. Linux CPU may be a second-class citizen.

---

## Phase 3: distributed-llama

**Source:** https://github.com/b4rtaz/distributed-llama

### What it does

Custom C++ implementation optimized for CPU clusters. Root node loads model, distributes weight slices to workers. Each worker processes its slice in parallel. Supports ARM NEON + x86 AVX2.

### Setup steps

1. **Build on both nodes:**
   ```bash
   git clone https://github.com/b4rtaz/distributed-llama
   cd distributed-llama
   make -j$(nproc)
   ```

2. **Convert model (if needed):**
   ```bash
   # distributed-llama may need its own format
   # Check README for GGUF compatibility or conversion steps
   python3 converter.py --input ~/models/Qwen3-30B-A3B-Q4_K_M.gguf --output model.dllama
   ```

3. **Start worker on titan-pc:**
   ```bash
   ./dllama worker --port 9998
   ```

4. **Start root on titan-pi:**
   ```bash
   ./dllama inference \
     --model model.dllama \
     --workers titan-pc:9998 \
     --prompt "You are a technical writer..."
   ```

5. Repeat with DeepSeek model.

### Key questions to answer

- Does it support GGUF directly or need conversion?
- Node count must be 2^n -- we have exactly 2, so it works. What if we add a 3rd node later?
- How does the tensor split compare to llama.cpp RPC?
- ARM NEON + x86 AVX2 in same cluster -- does it handle the architecture mismatch?
- Is there an OpenAI-compatible API server, or just CLI?

### Risk

Smaller community, less maintained. Model format compatibility unknown. Power-of-2 node constraint limits future scaling.

---

## Phase 4: Compare & Design Hybrid

### Comparison Matrix

After all 3 phases, fill in:

| Dimension | llama.cpp RPC | exo | distributed-llama |
|-----------|--------------|-----|-------------------|
| Setup complexity | | | |
| Mixed arch (ARM+x86) | | | |
| Qwen3-30B TTFT | | | |
| Qwen3-30B tok/s | | | |
| DeepSeek-32B TTFT | | | |
| DeepSeek-32B tok/s | | | |
| Peak RAM titan-pi | | | |
| Peak RAM titan-pc | | | |
| Network overhead | | | |
| Model load time | | | |
| API compatibility | | | |
| Scaling flexibility | | | |
| Code quality/maturity | | | |

### Hybrid Design Criteria

Cherry-pick the best from each:

- **Layer distribution strategy:** Which framework splits layers most efficiently for heterogeneous RAM?
- **Transport:** Which has lowest overhead for tensor data between nodes?
- **Model lifecycle:** Which manages model load/unload best?
- **API surface:** OpenAI-compatible is the target (llama-server already does this)
- **Integration with soul-mesh:** Must work with hub-agent model, JWT auth, executor, heartbeats

### Output

Phase 4 produces: `docs/plans/YYYY-MM-DD-distributed-inference-hybrid-design.md`

This becomes the spec for soul-mesh Layer 2 implementation.

---

## Execution Schedule

| Phase | Estimated time | Prerequisites |
|-------|---------------|---------------|
| Phase 1: llama.cpp RPC | 1 BUILD block (4h) | Models downloaded |
| Phase 2: exo | 1 BUILD block (4h) | Models available |
| Phase 3: distributed-llama | 1 BUILD block (4h) | Models available |
| Phase 4: Compare + Design | 1 EXPLORE block (4h) | Phases 1-3 complete |

**Pre-work (before Phase 1):**
- Download Qwen3-30B-A3B Q4_K_M GGUF (~18 GB)
- Download DeepSeek-R1-Distill-Qwen-32B Q4_K_M (~19 GB)
- Verify titan-pc SSH and port access from titan-pi
- Install build dependencies on both nodes (cmake, clang, python3)

## References

- [llama.cpp RPC README](https://github.com/ggml-org/llama.cpp/blob/master/tools/rpc/README.md)
- [llama.cpp distributed inference on ARM](https://learn.arm.com/learning-paths/servers-and-cloud-computing/distributed-inference-with-llama-cpp/)
- [exo GitHub](https://github.com/exo-explore/exo)
- [exo on SBCs and mixed clusters](https://www.cnx-software.com/2025/02/18/exo-software-a-distributed-llm-solution-running-on-a-cluster-of-computers-smartphones-or-sbcs/)
- [distributed-llama GitHub](https://github.com/b4rtaz/distributed-llama)
- [soul-mesh Layer 2 design](../soul-mesh/docs/plans/2026-02-23-layers-2-4-design.md)
