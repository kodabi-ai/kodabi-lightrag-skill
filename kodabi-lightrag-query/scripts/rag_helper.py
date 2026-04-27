#!/usr/bin/env python3
import asyncio
import sys

# Dinamik alan eşleştirme sözlüğü
DOMAIN_KEYWORDS = {
    "business_strategy": ["startup", "management", "strategy", "finance", "roadmap"],
    "software_engineering": ["LLMOps", "infrastructure", "pipeline", "code", "tech", "docker"],
    "legal": ["contract", "license", "copyright", "compliance"],
    "human": ["culture", "hr", "team", "people"]
}

def map_domains(query: str) -> list:
    """Sorgu içeriğine göre hedef MCP'leri dinamik olarak belirler."""
    domains = set()
    for domain, keywords in DOMAIN_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in query.lower():
                domains.add(domain)
    return list(domains) if domains else ["software_engineering"]  # Varsayılan

async def mock_fetch(domain: str, query: str) -> dict:
    """Simüle edilmiş MCP yanıtı. Gerçek ortamda HTTP/RPC çağrısı yapılır."""
    await asyncio.sleep(0.3)  # Network latency simülasyonu
    return {
        "references": [{"file_path": f"docs/{domain}.md", "title": f"{domain} Doc"}],
        "response": f"[Dynamic Context for '{domain}' | Query: '{query}']\nBu alan, ilgili domain için dinamik olarak toplanan bağlamı içerir."
    }

def format_injection(domain: str, data: dict, query: str) -> str:
    """Gelen veriyi Reasoning Chain'e enjekte edilecek XML formatına dönüştürür."""
    content = data['response'].replace("<", "&lt;").replace(">", "&gt;")
    refs = ", ".join([ref['title'] for ref in data['references']])
    return f'<rag_context source="{domain}" query_ref="{query}" refs="{refs}">\n{content}\n</rag_context>'

async def main(query: str):
    print(f"🚀 Kodabi RAG Helper v1.4.0 (Dynamic)")
    print(f"📝 Query: {query}\n")
    
    # 1. Dinamik Alan Eşleştirme
    domains = map_domains(query)
    print(f"🔍 Detected Domains: {', '.join(domains)}\n")
    
    # 2. Paralel Fetch (asyncio)
    tasks = [mock_fetch(d, query) for d in domains]
    results = await asyncio.gather(*tasks)
    
    # 3. Dinamik Formatlama & Injection
    formatted_blocks = [format_injection(d, r, query) for d, r in zip(domains, results)]
    final_context = "\n\n".join(formatted_blocks)
    
    print("--- REASONING CHAIN INJECTION ---\n")
    print(final_context)
    
    # 4. Sanity Check
    sanity = "✅ PASS" if len(final_context) > 100 else "⚠️ WARN"
    print(f"\n--- SANITY CHECK ---\n{sanity}: Context volume verified.")

if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "LLMOps startup strategy"
    asyncio.run(main(q))
