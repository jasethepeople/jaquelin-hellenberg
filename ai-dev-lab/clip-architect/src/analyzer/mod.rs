use serde::{Deserialize, Serialize};
use async_trait::async_trait;

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct ViralMoment {
    pub start_time: f64,
    pub end_time: f64,
    pub confidence: f32,
    pub tag: String,
    pub summary: String,
}

#[async_trait]
pub trait LlmClient {
    async fn analyze_chunk(&self, text: &str) -> Vec<ViralMoment>;
}

pub struct MockLlm;

#[async_trait]
impl LlmClient for MockLlm {
    async fn analyze_chunk(&self, _text: &str) -> Vec<ViralMoment> {
        // Simulates a viral moment without using any VRAM
        vec![ViralMoment {
            start_time: 10.5,
            end_time: 45.0,
            confidence: 0.95,
            tag: "insightful".to_string(),
            summary: "Mock analysis: High value segment detected.".to_string(),
        }]
    }
}

pub struct TranscriptChunker {
    window_size: usize,
    overlap: usize,
}

impl TranscriptChunker {
    pub fn new(window_size: usize, overlap: usize) -> Self {
        Self { window_size, overlap }
    }

    pub fn chunk_transcript(&self, text: &str) -> Vec<String> {
        let words: Vec<&str> = text.split_whitespace().collect();
        let mut chunks = Vec::new();
        let mut start = 0;

        while start < words.len() {
            let end = (start + self.window_size).min(words.len());
            chunks.push(words[start..end].join(" "));
            if end == words.len() { break; }
            start += self.window_size - self.overlap;
        }
        chunks
    }
}

pub struct RealLlm {
    pub api_base: String,
    pub model_name: String,
    pub client: reqwest::Client,
}

impl RealLlm {
    pub fn new(api_base: &str, model_name: &str) -> Self {
        Self {
            api_base: api_base.to_string(),
            model_name: model_name.to_string(),
            client: reqwest::Client::builder()
                .timeout(std::time::Duration::from_secs(60)) // Safety timeout
                .build()
                .unwrap(),
        }
    }
}

#[async_trait]
impl LlmClient for RealLlm {
    async fn analyze_chunk(&self, text: &str) -> Vec<ViralMoment> {
        let url = format!("{}/chat/completions", self.api_base);
        
        let payload = serde_json::json!({
            "model": self.model_name,
            "messages": [
                {
                    "role": "system", 
                    "content": "Analyze the transcript. Return ONLY a JSON array of objects with: start_time, end_time, confidence (0-1), tag, and summary."
                },
                {"role": "user", "content": text}
            ],
            "temperature": 0.3
        });

        match self.client.post(&url).json(&payload).send().await {
            Ok(resp) => {
                let json: serde_json::Value = resp.json().await.unwrap_or_default();
                // Basic parsing of the LLM response
                // (In a real app, we'd use a more robust regex/parser here)
                println!("Architect analyzed chunk via {}", self.model_name);
                vec![] // Placeholder for parsed results
            },
            Err(e) => {
                eprintln!("Error calling Architect: {}", e);
                vec![]
            }
        }
    }
}

pub struct HeatmapAggregator {
    pub min_gap: f64, // Seconds to bridge between close clips
}

impl HeatmapAggregator {
    pub fn new(min_gap: f64) -> Self {
        Self { min_gap }
    }

    pub fn merge_moments(&self, mut moments: Vec<ViralMoment>) -> Vec<ViralMoment> {
        if moments.is_empty() { return vec![]; }

        // 1. Sort by start time
        moments.sort_by(|a, b| a.start_time.partial_cmp(&b.start_time).unwrap());

        let mut merged: Vec<ViralMoment> = Vec::new();
        let mut current = moments[0].clone();

        for next in moments.into_iter().skip(1) {
            // 2. Check if overlapping or close enough to bridge
            if next.start_time <= current.end_time + self.min_gap {
                // Extend the current moment
                current.end_time = current.end_time.max(next.end_time);
                // Average the confidence
                current.confidence = (current.confidence + next.confidence) / 2.0;
                // Append summary
                current.summary = format!("{}; {}", current.summary, next.summary);
            } else {
                merged.push(current);
                current = next;
            }
        }
        merged.push(current);
        merged
    }
}
