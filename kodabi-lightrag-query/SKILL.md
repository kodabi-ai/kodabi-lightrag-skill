---
name: "kodabi-lightrag-query"
description: "Enrich reasoning chain by decomposing tasks, querying RAG microservices (loose coupling) with only_context=true, parallel execution, aggregation, and python automation."
version: "1.3.0"
author: "Kodabi"
tags: ["rag", "context-injection", "reasoning", "kodabi", "microservice", "parallel", "automation"]
trigger_patterns:
  - "kodabi lightrag query"
  - "search microservices"
  - "check context before acting"
  - "parallel rag query"
---

# Kodabi Lightrag Query v1.3.0

Bu beceri, bir aksiyona geçmeden önce LLM'nin reasoning chain'ine (düşünce zincirine) sağlam bir bağlam eklemek için tasarlanmıştır. Kodabi'ye özel veri yetersizse bile, görevi parçalayıp birden fazla RAG microservisinden (MCP) veri toplayarak, bağlamı zenginleştirir.

## Amaç

Kullanıcı isteğini alt sorgulara böl, uygun RAG microservislerine paralel olarak gönder, `only_context=true` ile ham veriyi çek, sonuçları birleştir/sağla ve reasoning chain'e enjekte et.

## İş Akışı

### 1. Görevi Parçala (Decompose)
Kullanıcının isteğini küçük, bağımsız sorgulanabilir parçalara böl.
- *Örn:* "LLMOps şirketi kur" -> "LLMOps strateji", "LLMOps teknik altyapı".
- Her parça için ayrı bir sorgu hazırla.

### 2. Microservis Seçimi (Loose Coupling)
Mutlaka sabit bir liste yerine, **`lightrag_..._mcp`** desenine uyan tüm mevcut araçları dinamik olarak ara.
- **Strateji & İş:** `lightrag_business_strategy_mcp`
- **Kod & Teknik:** `lightrag_software_engineering_mcp`
- **Yasal (Legal):** `lightrag_law_mcp`
- **Diğer:** Kullanıcı isteğine göre yeni eklenebilir microservisler.

### 3. Paralel RAG Sorgusu (Context Fetching)
Hazırladığın alt sorguları mümkün olan **en kısa sürede ve paralel olarak** başlat. **Mutlaka `only_context: true` gönder.**

**Araç:** `lightrag_..._mcp.query_document`
**Argümanlar:**
- `query`: Alt soru (Örn: "LLMops business strategy")
- `mode`: `mix`
- `only_context`: `true` (Kural: Her zaman true)
- `response_type`: `Multiple Paragraphs`
- `top_k`: 5

### 4. Sonuç Yönetimi ve Aggregation
Birden fazla microservisten gelen verileri aşağıdaki mantıkla birleştir:
- **Aynı Anlam (Merge):** İçerikler örtüşüyorsa, detayları tek bir kaynakta birleştir.
- **Farklı Detay (Supplement):** İki kaynak farklı yönleri vurguluyorsa, hepsini "Ek Bilgi" olarak zincire ekle.
- **Etiketleme:** Her cevabı XML etiketiyle sınırla: `<rag_context source="microservice_name">...</rag_context>`.

### 5. Nihali Aksiyon
Bilgi zenginleştirilmiş reasoning chain üzerinden yanıtı üret veya kodu yaz.

## Python Helper Script
`scripts/rag_helper.py` script'i paralel sorguları ve XML etiketlemeyi otomatize eder.
Kullanımı: `python rag_helper.py "<soru>"`

## Örnek Kullanım

**Giriş:** "LLMOps için gerekli adımları sırala."

1. **Parçala:** 1. `lightrag_business_strategy_mcp` sorgusu, 2. `lightrag_software_engineering_mcp` sorgusu.
2. **Paralel Sorgu:** Her iki MCP'ye de aynı anda `only_context=true` ile gönder.
3. **Aggregation:** Gelen verileri `<rag_context>` içine yerleştir.
4. **Sonuç:** Kod yazılır.
## İpuçları
- `only_context: true` kuralını asla bozma.
- Paralel sorgular için `asyncio` veya `rag_helper.py` kullan.
- RAG boş dönerse hemen `search_engine` devreye al.
- Çıktı formatı kullanıcıya net ve doğrudan kullanılabilir olmalı.
