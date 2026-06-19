# Changelog

## [0.1.3](https://github.com/NizardV/vigil/compare/v0.1.2...v0.1.3) (2026-06-19)


### Bug Fixes

* add actions write permission for workflow dispatch ([9a16bad](https://github.com/NizardV/vigil/commit/9a16bad50fb0b235f2849adf9b4554531637d63e))
* add actions write permission for workflow dispatch ([38083d6](https://github.com/NizardV/vigil/commit/38083d6fe70b8806a466050d4b59492725eee772))

## [0.1.2](https://github.com/NizardV/vigil/compare/v0.1.1...v0.1.2) (2026-06-19)


### Bug Fixes

* trigger deploy workflow from release-please ([211624a](https://github.com/NizardV/vigil/commit/211624aef967f30f8a34b263b6e2592c8a7b86d5))
* trigger deploy workflow from release-please ([ea5c777](https://github.com/NizardV/vigil/commit/ea5c77713c54798db7da3cee1d010394396da3b0))

## [0.1.1](https://github.com/NizardV/vigil/compare/v0.1.0...v0.1.1) (2026-06-19)


### Bug Fixes

* trigger deploy on release published ([3949a4a](https://github.com/NizardV/vigil/commit/3949a4a44baf4681ae7ff418789ad3f0aa7e09e0))
* trigger deploy on release published ([8159ba3](https://github.com/NizardV/vigil/commit/8159ba33c99fa69f7c01dc67381ce996e311241e))

## 0.1.0 (2026-06-19)


### Features

* add configurable digest schedule and fetch interval per theme/source ([3ec02d6](https://github.com/NizardV/vigil/commit/3ec02d6111158c8253e77d04c495b844bfb672b5))
* add Themes/Stats pages, Alembic migrations, .env.example ([16c4a3b](https://github.com/NizardV/vigil/commit/16c4a3b70d4334ed39d7d4061ae4e0fb6596e15b))
* add Webhooks page ([b58f7aa](https://github.com/NizardV/vigil/commit/b58f7aa9995440762368277b48626af0fa618830))
* configurable digest schedule and fetch interval from UI ([4f3eae1](https://github.com/NizardV/vigil/commit/4f3eae1a1187da87b1bbcde9d5158b168c0579ac))
* Discord interactive buttons for article feedback ([fdc17e9](https://github.com/NizardV/vigil/commit/fdc17e994c4276e1e8f2b11feb11eaaf6d1b3641))
* dynamic digest schedule and fetch interval from DB ([2860bf5](https://github.com/NizardV/vigil/commit/2860bf50d80272bf86a49900b4a5f8965e2115ff))
* initial project structure ([7141c9a](https://github.com/NizardV/vigil/commit/7141c9a6dd5d9bd90121ed0e4f8016392576a065))
* send Discord messages via bot token for interactive buttons ([1b41839](https://github.com/NizardV/vigil/commit/1b418391990c78019d34f089ed6260e3c3d4324c))
* send individual articles with Discord feedback buttons ([8406a34](https://github.com/NizardV/vigil/commit/8406a343a1b6aa9c8adb8aaa6ea090d415959209))


### Bug Fixes

* added more timeout to wait for the digest ([7f46eeb](https://github.com/NizardV/vigil/commit/7f46eeb68e989bcf84b4919c36b5a0099353b019))
* API_URL in Themes and Stats pages ([5d138e7](https://github.com/NizardV/vigil/commit/5d138e7b2039bd861692e5d6b0c5e172ab8f1ea8))
* change postgres exposed port to 5433 to avoid conflict with cyna-db ([28f983a](https://github.com/NizardV/vigil/commit/28f983af346a8f38682bdc669cd9097857e29fe2))
* encoding issues in tasks, llm, streamlit pages and dockerfile ([321c5b8](https://github.com/NizardV/vigil/commit/321c5b8f26c7a06e909391164dcaca81264f3f94))
* home page location and Dockerfile configuration for streamlit ([ba435d6](https://github.com/NizardV/vigil/commit/ba435d68867047eb0dfe2a0d6af334c7083c47ba))
* improve JSON parsing for Gemini 2.5, fix embedding dimensions to 384 ([33c30cc](https://github.com/NizardV/vigil/commit/33c30cc628336fa9d0e101b55dbb3815746b1701))
* lowercase image names for GHCR ([f084b4d](https://github.com/NizardV/vigil/commit/f084b4d84ea0d95e2f958ac2310f014e0a472536))
* streamlit pages encoding, switch to English, fix API_URL ([7475906](https://github.com/NizardV/vigil/commit/747590603b519c752e5714d152343e5aeb8a5dd7))
* use JSON mime type for Gemini, increase max tokens to 1024 ([34e0b2b](https://github.com/NizardV/vigil/commit/34e0b2be0df8c7a9808412827d68ebe18719efbc))


### Documentation

* add comprehensive English documentation ([84914df](https://github.com/NizardV/vigil/commit/84914df175b1ac60663ba7cf03b3ac9d99181920))
* rewrite README in English, fix encoding ([f437cb2](https://github.com/NizardV/vigil/commit/f437cb28e916359c7192b8ac80d4b761947b782c))
