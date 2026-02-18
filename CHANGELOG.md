# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-19

### Added

- Initial release
- Multi-function app for Discord server administration
- **Messages**: send_message, edit_message, delete_message
- **Channels**: get_channel, list_channels, create_channel
- **Guild**: get_guild
- **Roles**: list_roles, create_role, add_role, remove_role
- **Members**: get_member, set_nickname, ban_user, unban_user, kick_user
- **Webhooks**: create_webhook

### Dependencies

- aiohttp >= 3.9.0
- Python 3.11

### Configuration

- Requires DISCORD_BOT_TOKEN secret
- Default RAM: 2048MB
- Category: utility
