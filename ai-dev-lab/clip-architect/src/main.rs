pub mod analyzer;
pub mod export;
pub mod video;
pub mod config;

use analyzer::{LlmClient, MockLlm, TranscriptChunker, HeatmapAggregator};
use config::Config;
use video::VideoProcessor;
use std::fs;

#[tokio::main]
async fn main() {
    let conf = Config::load("config.toml").expect("Failed to load config.toml");
    let active_style = conf.style.get("tiktok").expect("TikTok style not found");

    let client = MockLlm;
    let chunker = TranscriptChunker::new(1000, 200);
    let aggregator = HeatmapAggregator::new(2.0);
    let processor = VideoProcessor::new();

    // Mock processing for demonstration
    let raw_moments = client.analyze_chunk("Exploring the center-crop logic.").await;
    let final_clips = aggregator.merge_moments(raw_moments);
    
    // 1. Generate the Styled Subtitles
    let ass_content = processor.generate_ass(&final_clips, active_style);
    fs::write("styled_captions.ass", ass_content).expect("Unable to write ASS");

    // 2. Generate the Vertical Crop Command
    let render_cmd = processor.create_vertical_crop_command(
        "podcast.mp4", 
        "styled_captions.ass", 
        "tiktok_ready.mp4"
    );

    println!("\n--- Vertical Export Ready ---");
    println!("Run the following command to generate your vertical TikTok clip:");
    println!("\n{}\n", render_cmd);
}
