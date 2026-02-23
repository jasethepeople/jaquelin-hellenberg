use crate::analyzer::ViralMoment;
use std::fs::File;
use std::io::Write;

pub struct ResolveExporter {
    pub project_name: String,
}

impl ResolveExporter {
    pub fn new(name: &str) -> Self {
        Self { project_name: name.to_string() }
    }

    pub fn generate_fcpxml(&self, moments: &[ViralMoment], source_path: &str) -> String {
        let mut xml = String::new();
        xml.push_str("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n");
        xml.push_str("<!DOCTYPE fcpxml>\n");
        xml.push_str("<fcpxml version=\"1.8\">\n");
        xml.push_str("  <resources>\n");
        xml.push_str("    <format id=\"r1\" name=\"FFVideoFormat1080p30\" frameDuration=\"100/3000s\"/>\n");
        xml.push_str(&format!("    <asset id=\"a1\" name=\"Source\" src=\"file://{}\" />\n", source_path));
        xml.push_str("  </resources>\n");
        xml.push_str("  <library>\n");
        xml.push_str(&format!("    <event name=\"{}\">\n", self.project_name));
        xml.push_str("      <project name=\"Generated Clips\">\n");
        xml.push_str("        <sequence format=\"r1\">\n");
        xml.push_str("          <spine>\n");

        for moment in moments {
            let duration = moment.end_time - moment.start_time;
            xml.push_str(&format!(
                "            <asset-clip ref=\"a1\" offset=\"0s\" name=\"{}\" start=\"{}s\" duration=\"{}s\" />\n",
                moment.tag, moment.start_time, duration
            ));
        }

        xml.push_str("          </spine>\n");
        xml.push_str("        </sequence>\n");
        xml.push_str("      </project>\n");
        xml.push_str("    </event>\n");
        xml.push_str("  </library>\n");
        xml.push_str("</fcpxml>");
        xml
    }

    pub fn save_to_disk(&self, content: &str, filename: &str) -> std::io::Result<()> {
        let mut file = File::create(filename)?;
        file.write_all(content.as_bytes())?;
        Ok(())
    }
}
