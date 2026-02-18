# Discord Admin Py

Discord server administration via inference.sh - Channel, role, member management, messages, and more.

## Quick Start

```bash
# Install CLI
curl -fsSL https://cli.inference.sh | sh && infsh login

# Set Discord Bot Token
# Add DISCORD_BOT_TOKEN in app settings after deployment
```

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

## Examples

### Send a Message

```bash
infsh app run user/discord-admin-py --function send_message --input '{
  "channel_id": "123456789012345678",
  "content": "Hello from inference.sh!"
}'
```

### List Channels

```bash
infsh app run user/discord-admin-py --function list_channels --input '{
  "guild_id": "123456789012345678"
}'
```

### Create a Role

```bash
infsh app run user/discord-admin-py --function create_role --input '{
  "guild_id": "123456789012345678",
  "name": "Moderator",
  "color": 16711680
}'
```

### Ban a User

```bash
infsh app run user/discord-admin-py --function ban_user --input '{
  "guild_id": "123456789012345678",
  "user_id": "987654321098765432",
  "reason": "Spamming",
  "delete_messages_days": 7
}'
```

## Setup

### Required Permissions

Your Discord bot needs these permissions:

- `MANAGE_CHANNELS` - For channel operations
- `MANAGE_ROLES` - For role operations
- `KICK_MEMBERS` - For kicking users
- `BAN_MEMBERS` - For banning users
- `MANAGE_MESSAGES` - For message operations
- `VIEW_AUDIT_LOG` - For audit logs (optional)

### Bot Token

Set `DISCORD_BOT_TOKEN` in the app's secrets configuration after deployment.

## Development

```bash
# Test locally
infsh app dev --function send_message --input '{"channel_id": "123", "content": "test"}'

# Validate functions
infsh app validate
```

## Related

- [Discord Developer Portal](https://discord.com/developers/docs)
- [inference.sh Docs](https://inference.sh/docs)
