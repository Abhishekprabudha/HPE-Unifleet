# HPE-Unifleet

## Narration audio workflow
Run GitHub Action **Build narration audio** to generate `audio/unifleet-complete-narration.mp3` using a British female neural voice (`en-GB-SoniaNeural`). The narration text is taken from `unifleet-narration.html`.

## Narrated Global Airlines video workflow

1. Open the repository's **Actions** tab and select **Build narrated Global Airlines video**.
2. Select **Run workflow**.
3. When the run finishes, open it and download the **global-airlines-with-narration** artifact.

The workflow reads the default narration from `unifleet-narration.html`, generates a
British female voice-over, loops `Global Airlines.mp4` to match the narration, and
exports `video/global-airlines-with-narration.mp4`. If the source video has audio,
it is retained quietly beneath the narration. The downloadable artifact is kept
for 30 days.
