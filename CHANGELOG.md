# Changelog

All notable changes to this project will be documented in this file.

## [1.3.2](https://github.com/linuxgoose/mataroa/releases/tag/1.3.2)
* add blog index content by @linuxgoose in https://github.com/linuxgoose/mataroa/pull/23
* [add custom robots.txt blog setting](https://github.com/linuxgoose/mataroa/commit/47bd06b3a71d75ddf73a91958b2e3101c675633e) by @linuxgoose
* [add custom posts page title](https://github.com/linuxgoose/mataroa/commit/3ac28fdb08b59310c6fcc313a6af511320a66f50)
* [add more feed urls](https://github.com/linuxgoose/mataroa/commit/b57c9d0b06642b4983258ffd2bdf57cd18d49613) by @linuxgoose
* [add noindex support - meta tag](https://github.com/linuxgoose/mataroa/commit/dcbd6e2360068953bcd72910c76574b4a63a35a0) by @linuxgoose
* [add ability to set post_backups_on in blog settings](https://github.com/linuxgoose/mataroa/commit/ac590b7092b9786b1d7e4d1cb6aa6a7c88937237) by @linuxgoose
* [add blog index content](https://github.com/linuxgoose/mataroa/commit/f480264f048edbf0b9164388e3a77de95c48fc55) by @linuxgoose

## [1.3.1](https://github.com/linuxgoose/mataroa/releases/tag/1.3.1)
* Add LaTeX Support with l2m4m dependency & mathml

## [1.3.0](https://github.com/mataroablog/mataroa/compare/v1.2...v1.3)

### Important changes

* Rebuild content moderation dashboard with:
    * pagination
    * filters
    * sort by
    * day summary
    * images overview
    * global stats
    * daily admin summary email
* Switch to astral uv
* Add hard check for image uploading limit
* Change sign up text
* Remove robot checks from sign up form
* Upgrade to Django 5.2
* Add docker image auto-push to ghcr.io

### Bug fixes

* Improve dark mode colours for better readability
* Fix ansible not auto-enabling systemd timers

## [1.2.0](https://github.com/mataroablog/mataroa/compare/v1.1...v1.2) - 2025-02-06

### Important changes

* Change project license from MIT to AGPL-3.0-only
* Enable customisation of subscribe note on footer
* Introduce ansible configuration for deployment
* Switch jobs from cron to systemd timers
* Replace uWSGI with Gunicorn
* Replace black/flake8/isort with ruff
* Refactor newsletter processing into more robust and simpler workflow
* Setup docs using mdbook
* Improve docker local development setup
* Add guide for custom domains
* Simplify Zola and Hugo base CSS styles
* Add themed error pages
* Upgrade to Django 5.1
* Limit RSS to last 10 posts

### Bugfixes

* Fix Zola v0.19 RSS feed configuration

## [1.1.0](https://github.com/mataroablog/mataroa/compare/v1.0...v1.1) - 2023-12-05

### Important changes

* Rewrite moderation dashboard
* Rewrite Stripe integration with latest APIs
* Create new signup workflow
* Lower image size limit to 1MB
* Upgrade to Django 5.0

## [1.0.0](https://github.com/mataroablog/mataroa/compare/5ff277da71fb653631ea38407cd6154e831be540...v1.0) - 2023-09-06

This is an initial numbered release after 3+ years of development.

* Core blogging functionalities
* Export functionalities
* Email newsletter
* Custom domains
* Backend-based analytics
* API
