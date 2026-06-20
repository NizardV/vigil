# Changelog

## [0.4.0](https://github.com/NizardV/vigil/compare/v0.3.0...v0.4.0) (2026-06-20)


### Features

* add auth models and dependencies ([cf20cd9](https://github.com/NizardV/vigil/commit/cf20cd93d99f97ef62a6aef017d6cd713211a063))
* add auth service and routes ([7ee678d](https://github.com/NizardV/vigil/commit/7ee678df27bcd1b1f7d72aa0d0ba991ea2824160))
* add Streamlit auth UI with login, register and TOTP ([73da0a5](https://github.com/NizardV/vigil/commit/73da0a520b69f20661848b0374dd9ae83411739a))
* add TOTP settings page and fix user email in session ([108afa8](https://github.com/NizardV/vigil/commit/108afa8747c40625ef54535daccd21a10693415a))
* implement TOTP enable/disable ([eb6b48d](https://github.com/NizardV/vigil/commit/eb6b48d15872925ae831d2c6b4630da7f05d441e))
* persist session with cookies ([9577b1d](https://github.com/NizardV/vigil/commit/9577b1d449b0c09a14f868a5bff5c61b91901154))
* refactor Streamlit navigation with app.py entry point and email confirmation page ([9b71089](https://github.com/NizardV/vigil/commit/9b71089e9007136d2d863e350d2cb3bedf37688b))
* session persistence via Redis httpOnly cookie and streamlit-js-eval ([4e7bbe3](https://github.com/NizardV/vigil/commit/4e7bbe3b177178df4486f94cd02a9060c538495c))


### Bug Fixes

* changed email confirmation path ([f6b7d44](https://github.com/NizardV/vigil/commit/f6b7d443cc215803ec5aa0c42db3d1cdf2e64989))
* cookie instanciation duplication ([4993153](https://github.com/NizardV/vigil/commit/4993153c234d07a57798dafd0578f0482f14c64d))
* cookie management ([ba16aba](https://github.com/NizardV/vigil/commit/ba16aba7e1f1fe376f295e3a918c8ab89dc0bc9b))
* cookie set use max age instead of expires at ([bfa0dee](https://github.com/NizardV/vigil/commit/bfa0dee591bfe79d9f00ffe448dc7f3b5bac22d7))
* library bycrypt auth changed due to passlib bug on python 3.12 ([3a0a784](https://github.com/NizardV/vigil/commit/3a0a784aee35aa07233e33838f739d45b303e8bd))
* migration - clear data before adding user_id NOT NULL columns ([7ed9dcc](https://github.com/NizardV/vigil/commit/7ed9dcc696488495b01181da37a044a598edecfc))
* migration - clear data before adding user_id NOT NULL columns updated ([46952d8](https://github.com/NizardV/vigil/commit/46952d8400ec81d49b18a2e522c8cdb249714101))
* remove require_auth from pages, handled by app.py navigation ([eb41f84](https://github.com/NizardV/vigil/commit/eb41f84bb51dd1127f4b2341608e570c48ee0598))
* rename pages to lowercase ([2704851](https://github.com/NizardV/vigil/commit/27048510ddfe0bc1b8ab898c175351e16af03c55))
* session restore for cookies ([205f3d3](https://github.com/NizardV/vigil/commit/205f3d3ac5211340d8968ab9baecfd50d489f415))
* session state ([eebddea](https://github.com/NizardV/vigil/commit/eebddead8e59c83b1817f4b264a649cddc8bca98))
* session time management ([732f8e2](https://github.com/NizardV/vigil/commit/732f8e224d4d267eb1fb89c09bf567498ef9381d))
* set cookie removed ([ebe542d](https://github.com/NizardV/vigil/commit/ebe542dfe46f943f398c45f1badabbe985fbb53d))
* single CookieController instance to avoid session state conflict ([8904be5](https://github.com/NizardV/vigil/commit/8904be5e15db6627e39d76b8cfb9cd37deeb71d4))
* spinner for restoring session ([26ce550](https://github.com/NizardV/vigil/commit/26ce550d78d9421040f9d8ad7cdaa7e7ab622dac))
* timezone problem in auth service ([e8e632a](https://github.com/NizardV/vigil/commit/e8e632ad3fa7b4f3e2357f1d3b32bf8d8e5b7bde))
* update version of streamlit for navigation ([86d1efc](https://github.com/NizardV/vigil/commit/86d1efc5bd625669149f2e6b56b58473f815632b))
* user mail link disabled ([7a4b439](https://github.com/NizardV/vigil/commit/7a4b439efec7618edf932dbb33623d2e5df5676e))

## [0.3.0](https://github.com/NizardV/vigil/compare/v0.2.0...v0.3.0) (2026-06-19)


### Features

* use torch CPU-only to reduce image size ([6f9b8df](https://github.com/NizardV/vigil/commit/6f9b8df63cf92913506c94db3e827fb0fd922425))


### Bug Fixes

* codeql-action v4 and security-events permission ([3a84f30](https://github.com/NizardV/vigil/commit/3a84f3022f2a79ec16a4483765e34f7e14e40d45))

## [0.2.0](https://github.com/NizardV/vigil/compare/v0.1.3...v0.2.0) (2026-06-19)


### Features

* upload Trivy scan results to GitHub Security tab ([0d99ef5](https://github.com/NizardV/vigil/commit/0d99ef5a7e675eda36d11de3fb6aa7a7556c35bc))
* upload Trivy scan results to GitHub Security tab ([ff47cd2](https://github.com/NizardV/vigil/commit/ff47cd2376cabf635f6512b889492bd9582fd14a))

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
