# Artifact — the cost-per-question calculator

Price any RAG flow in five steps:

- [ ] `count_tokens(text)` — 4 characters ≈ 1 token
- [ ] Pricing table: per-1M-token prices for input, output, and embedding
- [ ] `call_cost = (in_tokens × in_price + out_tokens × out_price) / 1_000_000`
- [ ] Compare retrieval cost vs model call cost — expect the 150-400x band
- [ ] Run the 1,000-question math with your real hit rate — quote the savings
