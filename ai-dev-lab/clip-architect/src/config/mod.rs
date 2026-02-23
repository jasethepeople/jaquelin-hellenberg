use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize, Serialize)]
pub struct SubtitleStyle {
    pub font_name: String,
    pub font_size: u32,
    pub primary_color: String,
    pub outline_color: String,
    pub alignment: u32,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct Config {
    pub style: std::collections::HashMap<String, SubtitleStyle>,
}

impl Config {
    pub fn load(path: &str) -> Result<Self, Box<dyn std::error::Error>> {
        let content = std::fs::read_to_string(path)?;
        let config: Config = toml::from_str(&content)?;
        Ok(config)
    }
}
