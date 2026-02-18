# Discord Admin Py

[![inference.sh app](https://img.shields.io/badge/inference.sh-app-blue)](https://inference.sh)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](https://github.com/JungHoonGhae/discord-admin-py/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/JungHoonGhae/discord-admin-py)](https://github.com/JungHoonGhae/discord-admin-py/stargazers)

Discord server administration via inference.sh — Multi-function app for channel, role, member management, messages, webhooks, and more.

## Why Discord Admin Py?

| Problem | Solution |
|---------|----------|
| Manual server management | Automate via AI agents |
| Repetitive moderation tasks | Script repeated actions |
| Cross-server management | Single API for multiple servers |

**Discord Admin Py** provides a unified interface to manage Discord servers through AI agents, powered by inference.sh.

## Features

- **Messages** — Send, edit, delete messages
- **Channels** — Create, list, get channel info
- **Roles** — Create, list, assign, remove roles
- **Members** — Get info, set nickname, ban, unban, kick
- **Guilds** — Get server information
- **Webhooks** — Create webhooks for automation

## Quick Start

```bash
# Install CLI
curl -fsSL https://cli.inference.sh | sh && infsh login

# Set Discord Bot Token
# Add DISCORD_BOT_TOKEN in app settings after deployment
```

## Installation

### Via inference.sh Grid

1. Visit [inference.sh Apps](https://app.inference.sh/apps)
2. Search for "discord-admin-py"
3. Add to your agent

### Via GitHub

```bash
# Clone the repository
git clone https://github.com/JungHoonGhae/discord-admin-py.git
cd discord-admin-py
```

## Configuration

### Required: Discord Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to Bot section and create a bot
4. Copy the token
5. Add to inference.sh app secrets as `DISCORD_BOT_TOKEN`

### Required Bot Permissions

Your Discord bot needs these permissions:

- `MANAGE_CHANNELS` — Channel operations
- `MANAGE_ROLES` — Role operations
- `KICK_MEMBERS` — Kick users
- `BAN_MEMBERS` — Ban users
- `MANAGE_MESSAGES` — Message operations
- `VIEW_AUDIT_LOG` — Audit logs (optional)

## Available Functions

### Messages

| Function | Description |
|----------|-------------|
| `send_message` | Send a message to a channel |
| `edit_message` | Edit an existing message |
| `delete_message` | Delete a message |

### Channels

| Function | Description |
|----------|-------------|
| `get_channel` | Get channel information |
| `list_channels` | List all channels in a guild |
| `create_channel` | Create a new channel |

### Guild

| Function | Description |
|----------|-------------|
| `get_guild` | Get guild (server) information |

### Roles

| Function | Description |
|----------|-------------|
| `list_roles` | List all roles in a guild |
| `create_role` | Create a new role |
| `add_role` | Assign a role to a user |
| `remove_role` | Remove a role from a user |

### Members

| Function | Description |
|----------|-------------|
| `get_member` | Get member information |
| `set_nickname` | Set a member's nickname |
| `ban_user` | Ban a user from the guild |
| `unban_user` | Unban a user |
| `kick_user` | Kick a user from the guild |

### Webhooks

| Function | Description |
|----------|-------------|
| `create_webhook` | Create a webhook in a channel |

## Usage Examples

### Send a Message

```bash
infsh app run JungHoonGhae/discord-admin-py --function send_message --input '{
  "channel_id": "123456789012345678",
  "content": "Hello from inference.sh!"
}'
```

### List Channels

```bash
infsh app run JungHoonGhae/discord-admin-py --function list_channels --input '{
  "guild_id": "123456789012345678"
}'
```

### Create a Role

```bash
infsh app run JungHoonGhae/discord-admin-py --function create_role --input '{
  "guild_id": "123456789012345678",
  "name": "Moderator",
  "color": 16711680
}'
```

### Ban a User

```bash
infsh app run JungHoonGhae/discord-admin-py --function ban_user --input '{
  "guild_id": "123456789012345678",
  "user_id": "987654321098765432",
  "reason": "Spamming",
  "delete_messages_days": 7
}'
```

## Development

### Prerequisites

- Python 3.11+
- [inference.sh CLI](https://cli.inference.sh)

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Test locally
infsh app dev --function send_message --input '{"channel_id": "123", "content": "test"}'

# Validate functions
infsh app validate
```

### Deploy

```bash
infsh app deploy
```

## Project Structure

```
discord-admin-py/
├── inf.yml              # App configuration
├── inference.py        # Main app logic (16 functions)
├── requirements.txt    # Python dependencies
├── LICENSE             # MIT License
├── VERSION            # Semantic version
├── CHANGELOG.md       # Version history
├── README.md          # This file
└── skills/            # AI agent guidance
    └── discord-admin-py.md
```

## License

MIT — See [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Feel free to submit a Pull Request.

## Legal Notice

This project is provided "as is" without warranty of any kind. Use of this app is subject to Discord's [Terms of Service](https://discord.com/terms) and [Developer Terms](https://discord.com/developers/docs/policies-and-agreements/developer-terms-of-service). Users are responsible for ensuring their usage complies with all applicable terms and conditions.

## Support

If this tool helps you, consider supporting its maintenance:

[![Buy Me A Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/lucas.ghae)

## Links

- [inference.sh](https://inference.sh) — AI agent runtime
- [Discord Developer Portal](https://discord.com/developers/docs)
- [Report Issues](https://github.com/JungHoonGhae/discord-admin-py/issues)

---

Built with [inference.sh](https://inference.sh) — The agent runtime.
