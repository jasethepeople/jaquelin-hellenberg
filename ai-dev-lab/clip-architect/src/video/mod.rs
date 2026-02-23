use crate::analyzer::ViralMoment;

pub struct VideoProcessor {
    pub ffmpeg_path: String,
}

impl VideoProcessor {
    pub fn new() -> Self {
        Self { ffmpeg_path: "ffmpeg".to_string() }
    }

    pub fn generate_ass(&self, moments: &[ViralMoment], style: &crate::config::SubtitleStyle) -> String {
        let mut ass = String::from("[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\n\n");
        ass.push_str("[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, Alignment\n");
        ass.push_str(&format!("Style: Default,{},{},{},{},{}\n\n", 
            style.font_name, style.font_size, style.primary_color, style.outline_color, style.alignment));
        ass.push_str("[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n");

        for moment in moments {
            ass.push_str(&format!("Dialogue: 0,{},{},Default,,0,0,0,,{}\n",
                self.format_ass_time(moment.start_time),
                self.format_ass_time(moment.end_time),
                moment.summary));
        }
        ass
    }

    fn format_ass_time(&self, seconds: f64) -> String {
        let hours = (seconds / 3600.0) as u32;
        let mins = ((seconds % 3600.0) / 60.0) as u32;
        let secs = (seconds % 60.0) as u32;
        let centis = ((seconds % 1.0) * 100.0) as u32;
        format!("{}:{:02}:{:02}.{:02}", hours, mins, secs, centis)
    }

    pub fn create_vertical_crop_command(&self, source: &str, ass_path: &str, output: &str) -> String {
        let filter = format!("crop=ih*9/16:ih:(iw-ow)/2:0,scale=1080:1920,subtitles={}", ass_path);
        format!("{} -hwaccel auto -i {} -vf \"{}\" -c:v libx264 -preset fast -c:a copy {} -y",
            self.ffmpeg_path, source, filter, output)
    }
}
