from inferencesh import BaseApp, BaseAppInput, BaseAppOutput, File
from pydantic import Field
from typing import Optional
import aiohttp
import os

# ============================================================================
# Input Schemas
# ============================================================================

class SendMessageInput(BaseAppInput):
    channel_id: str = Field(description="Discord channel ID (snowflake)")
    content: str = Field(description="Message content to send")


class SendMessageOutput(BaseAppOutput):
    message_id: str = Field(description="Created message ID")
    channel_id: str = Field(description="Channel ID where message was sent")


class EditMessageInput(BaseAppInput):
    channel_id: str = Field(description="Discord channel ID")
    message_id: str = Field(description="Message ID to edit")
    content: str = Field(description="New message content")


class EditMessageOutput(BaseAppOutput):
    message_id: str = Field(description="Edited message ID")
    updated: bool = Field(description="Whether message was updated")


class DeleteMessageInput(BaseAppInput):
    channel_id: str = Field(description="Discord channel ID")
    message_id: str = Field(description="Message ID to delete")


class DeleteMessageOutput(BaseAppOutput):
    deleted: bool = Field(description="Whether message was deleted")


class GetChannelInput(BaseAppInput):
    channel_id: str = Field(description="Discord channel ID")


class GetChannelOutput(BaseAppOutput):
    id: str
    name: str
    type: int
    position: Optional[int] = None
    topic: Optional[str] = None
    nsfw: Optional[bool] = None


class ListChannelsInput(BaseAppInput):
    guild_id: str = Field(description="Discord guild (server) ID")


class ListChannelsOutput(BaseAppOutput):
    channels: list = Field(description="List of channels in the guild")


class CreateChannelInput(BaseAppInput):
    guild_id: str = Field(description="Discord guild ID")
    name: str = Field(description="Channel name")
    channel_type: str = Field(default="text", description="Channel type: text, voice, category")


class CreateChannelOutput(BaseAppOutput):
    channel_id: str = Field(description="Created channel ID")
    name: str = Field(description="Channel name")
    type: int = Field(description="Channel type")


class GetGuildInput(BaseAppInput):
    guild_id: str = Field(description="Discord guild ID")


class GetGuildOutput(BaseAppOutput):
    id: str
    name: str
    icon: Optional[str] = None
    banner: Optional[str] = None
    description: Optional[str] = None
    approximate_member_count: Optional[int] = None


class ListRolesInput(BaseAppInput):
    guild_id: str = Field(description="Discord guild ID")


class ListRolesOutput(BaseAppOutput):
    roles: list = Field(description="List of roles in the guild")


class CreateRoleInput(BaseAppInput):
    guild_id: str = Field(description="Discord guild ID")
    name: str = Field(description="Role name")
    color: Optional[int] = Field(default=0, description="Role color (hex integer)")
    permissions: Optional[str] = Field(default="0", description="Permission bitwise string")


class CreateRoleOutput(BaseAppOutput):
    role_id: str = Field(description="Created role ID")
    name: str = Field(description="Role name")


class AddRoleInput(BaseAppInput):
    guild_id: str = Field(description="Discord guild ID")
    user_id: str = Field(description="User ID to assign role")
    role_id: str = Field(description="Role ID to assign")


class AddRoleOutput(BaseAppOutput):
    user_id: str
    role_id: str
    success: bool


class RemoveRoleInput(BaseAppInput):
    guild_id: str = Field(description="Discord guild ID")
    user_id: str = Field(description="User ID")
    role_id: str = Field(description="Role ID to remove")


class RemoveRoleOutput(BaseAppOutput):
    user_id: str
    role_id: str
    success: bool


class GetMemberInput(BaseAppInput):
    guild_id: str = Field(description="Discord guild ID")
    user_id: str = Field(description="User ID")


class GetMemberOutput(BaseAppOutput):
    user_id: str
    nick: Optional[str] = None
    roles: list
    joined_at: Optional[str] = None


class SetNicknameInput(BaseAppInput):
    guild_id: str = Field(description="Discord guild ID")
    user_id: str = Field(description="User ID")
    nick: str = Field(description="New nickname (empty to reset)")


class SetNicknameOutput(BaseAppOutput):
    user_id: str
    nick: Optional[str]


class BanUserInput(BaseAppInput):
    guild_id: str = Field(description="Discord guild ID")
    user_id: str = Field(description="User ID to ban")
    reason: Optional[str] = Field(default=None, description="Ban reason")
    delete_messages_days: Optional[int] = Field(default=0, description="Days of messages to delete (0-7)")


class BanUserOutput(BaseAppOutput):
    user_id: str
    banned: bool


class UnbanUserInput(BaseAppInput):
    guild_id: str = Field(description="Discord guild ID")
    user_id: str = Field(description="User ID to unban")


class UnbanUserOutput(BaseAppOutput):
    user_id: str
    unbanned: bool


class KickUserInput(BaseAppInput):
    guild_id: str = Field(description="Discord guild ID")
    user_id: str = Field(description="User ID to kick")
    reason: Optional[str] = Field(default=None, description="Kick reason")


class KickUserOutput(BaseAppOutput):
    user_id: str
    kicked: bool


class CreateWebhookInput(BaseAppInput):
    channel_id: str = Field(description="Discord channel ID")
    name: str = Field(description="Webhook name")


class CreateWebhookOutput(BaseAppOutput):
    webhook_id: str
    name: str
    token: Optional[str] = None


class ExecuteWebhookInput(BaseAppInput):
    webhook_id: str = Field(description="Webhook ID")
    content: str = Field(description="Message content")
    username: Optional[str] = Field(default=None, description="Override username")
    avatar_url: Optional[str] = Field(default=None, description="Override avatar")


class ExecuteWebhookOutput(BaseAppOutput):
    sent: bool
    message_id: Optional[str] = None


# ============================================================================
# App
# ============================================================================

class App(BaseApp):
    API_BASE = "https://discord.com/api/v10"
    
    def __init__(self):
        self.token = None
        self.session = None
    
    async def setup(self, metadata):
        """Initialize Discord bot token and aiohttp session."""
        self.token = os.environ.get("DISCORD_BOT_TOKEN")
        if not self.token:
            raise ValueError("DISCORD_BOT_TOKEN not set in secrets")
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bot {self.token}",
                "Content-Type": "application/json"
            }
        )
    
    async def unload(self):
        """Cleanup aiohttp session."""
        if self.session:
            await self.session.close()
    
    def _validate_snowflake(self, name: str, value: str):
        """Validate Discord snowflake ID (17-20 digits)."""
        if not value or not value.isdigit() or not (17 <= len(value) <= 20):
            raise ValueError(f"Invalid {name}: '{value}' (expected 17-20 digit snowflake)")
    
    async def _request(self, method: str, endpoint: str, data: Optional[dict] = None):
        """Make API request with error handling."""
        url = f"{self.API_BASE}{endpoint}"
        
        async with self.session.request(method, url, json=data if data else None) as resp:
            text = await resp.text()
            
            if resp.status == 204:
                return {"success": True}
            
            if resp.status >= 400:
                raise RuntimeError(f"Discord API error {resp.status}: {text[:200]}")
            
            import json
            return json.loads(text) if text else {}
    
    # =========================================================================
    # Messages
    # =========================================================================
    
    async def send_message(self, input_data: SendMessageInput, metadata) -> SendMessageOutput:
        """Send a message to a Discord channel."""
        self._validate_snowflake("channel_id", input_data.channel_id)
        
        metadata.log(f"Sending message to channel {input_data.channel_id}")
        
        result = await self._request(
            "POST",
            f"/channels/{input_data.channel_id}/messages",
            {"content": input_data.content}
        )
        
        return SendMessageOutput(
            message_id=result.get("id", ""),
            channel_id=input_data.channel_id
        )
    
    async def edit_message(self, input_data: EditMessageInput, metadata) -> EditMessageOutput:
        """Edit an existing message."""
        self._validate_snowflake("channel_id", input_data.channel_id)
        self._validate_snowflake("message_id", input_data.message_id)
        
        metadata.log(f"Editing message {input_data.message_id}")
        
        await self._request(
            "PATCH",
            f"/channels/{input_data.channel_id}/messages/{input_data.message_id}",
            {"content": input_data.content}
        )
        
        return EditMessageOutput(
            message_id=input_data.message_id,
            updated=True
        )
    
    async def delete_message(self, input_data: DeleteMessageInput, metadata) -> DeleteMessageOutput:
        """Delete a message."""
        self._validate_snowflake("channel_id", input_data.channel_id)
        self._validate_snowflake("message_id", input_data.message_id)
        
        metadata.log(f"Deleting message {input_data.message_id}")
        
        await self._request(
            "DELETE",
            f"/channels/{input_data.channel_id}/messages/{input_data.message_id}"
        )
        
        return DeleteMessageOutput(deleted=True)
    
    # =========================================================================
    # Channels
    # =========================================================================
    
    async def get_channel(self, input_data: GetChannelInput, metadata) -> GetChannelOutput:
        """Get channel information."""
        self._validate_snowflake("channel_id", input_data.channel_id)
        
        result = await self._request("GET", f"/channels/{input_data.channel_id}")
        
        return GetChannelOutput(
            id=result.get("id", ""),
            name=result.get("name", ""),
            type=result.get("type", 0),
            position=result.get("position"),
            topic=result.get("topic"),
            nsfw=result.get("nsfw")
        )
    
    async def list_channels(self, input_data: ListChannelsInput, metadata) -> ListChannelsOutput:
        """List all channels in a guild."""
        self._validate_snowflake("guild_id", input_data.guild_id)
        
        metadata.log(f"Listing channels for guild {input_data.guild_id}")
        
        result = await self._request("GET", f"/guilds/{input_data.guild_id}/channels")
        
        return ListChannelsOutput(channels=result)
    
    async def create_channel(self, input_data: CreateChannelInput, metadata) -> CreateChannelOutput:
        """Create a new channel."""
        self._validate_snowflake("guild_id", input_data.guild_id)
        
        # Map channel type to Discord integer
        type_map = {
            "text": 0,
            "voice": 2,
            "category": 4,
            "forum": 15,
            "stage": 13
        }
        channel_type_int = type_map.get(input_data.channel_type.lower(), 0)
        
        metadata.log(f"Creating {input_data.channel_type} channel: {input_data.name}")
        
        result = await self._request(
            "POST",
            f"/guilds/{input_data.guild_id}/channels",
            {
                "name": input_data.name,
                "type": channel_type_int
            }
        )
        
        return CreateChannelOutput(
            channel_id=result.get("id", ""),
            name=result.get("name", ""),
            type=result.get("type", 0)
        )
    
    # =========================================================================
    # Guild
    # =========================================================================
    
    async def get_guild(self, input_data: GetGuildInput, metadata) -> GetGuildOutput:
        """Get guild (server) information."""
        self._validate_snowflake("guild_id", input_data.guild_id)
        
        result = await self._request(
            "GET", 
            f"/guilds/{input_data.guild_id}?with_counts=true"
        )
        
        return GetGuildOutput(
            id=result.get("id", ""),
            name=result.get("name", ""),
            icon=result.get("icon"),
            banner=result.get("banner"),
            description=result.get("description"),
            approximate_member_count=result.get("approximate_member_count")
        )
    
    # =========================================================================
    # Roles
    # =========================================================================
    
    async def list_roles(self, input_data: ListRolesInput, metadata) -> ListRolesOutput:
        """List all roles in a guild."""
        self._validate_snowflake("guild_id", input_data.guild_id)
        
        result = await self._request("GET", f"/guilds/{input_data.guild_id}/roles")
        
        return ListRolesOutput(roles=result)
    
    async def create_role(self, input_data: CreateRoleInput, metadata) -> CreateRoleOutput:
        """Create a new role."""
        self._validate_snowflake("guild_id", input_data.guild_id)
        
        metadata.log(f"Creating role: {input_data.name}")
        
        result = await self._request(
            "POST",
            f"/guilds/{input_data.guild_id}/roles",
            {
                "name": input_data.name,
                "color": input_data.color,
                "permissions": input_data.permissions
            }
        )
        
        return CreateRoleOutput(
            role_id=result.get("id", ""),
            name=result.get("name", "")
        )
    
    async def add_role(self, input_data: AddRoleInput, metadata) -> AddRoleOutput:
        """Assign a role to a user."""
        self._validate_snowflake("guild_id", input_data.guild_id)
        self._validate_snowflake("user_id", input_data.user_id)
        self._validate_snowflake("role_id", input_data.role_id)
        
        metadata.log(f"Adding role {input_data.role_id} to user {input_data.user_id}")
        
        await self._request(
            "PUT",
            f"/guilds/{input_data.guild_id}/members/{input_data.user_id}/roles/{input_data.role_id}"
        )
        
        return AddRoleOutput(
            user_id=input_data.user_id,
            role_id=input_data.role_id,
            success=True
        )
    
    async def remove_role(self, input_data: RemoveRoleInput, metadata) -> RemoveRoleOutput:
        """Remove a role from a user."""
        self._validate_snowflake("guild_id", input_data.guild_id)
        self._validate_snowflake("user_id", input_data.user_id)
        self._validate_snowflake("role_id", input_data.role_id)
        
        metadata.log(f"Removing role {input_data.role_id} from user {input_data.user_id}")
        
        await self._request(
            "DELETE",
            f"/guilds/{input_data.guild_id}/members/{input_data.user_id}/roles/{input_data.role_id}"
        )
        
        return RemoveRoleOutput(
            user_id=input_data.user_id,
            role_id=input_data.role_id,
            success=True
        )
    
    # =========================================================================
    # Members
    # =========================================================================
    
    async def get_member(self, input_data: GetMemberInput, metadata) -> GetMemberOutput:
        """Get member information."""
        self._validate_snowflake("guild_id", input_data.guild_id)
        self._validate_snowflake("user_id", input_data.user_id)
        
        result = await self._request(
            "GET",
            f"/guilds/{input_data.guild_id}/members/{input_data.user_id}"
        )
        
        return GetMemberOutput(
            user_id=result.get("user", {}).get("id", ""),
            nick=result.get("nick"),
            roles=result.get("roles", []),
            joined_at=result.get("joined_at")
        )
    
    async def set_nickname(self, input_data: SetNicknameInput, metadata) -> SetNicknameOutput:
        """Set a member's nickname."""
        self._validate_snowflake("guild_id", input_data.guild_id)
        self._validate_snowflake("user_id", input_data.user_id)
        
        metadata.log(f"Setting nickname for user {input_data.user_id}")
        
        await self._request(
            "PATCH",
            f"/guilds/{input_data.guild_id}/members/{input_data.user_id}",
            {"nick": input_data.nick if input_data.nick else None}
        )
        
        return SetNicknameOutput(
            user_id=input_data.user_id,
            nick=input_data.nick if input_data.nick else None
        )
    
    async def ban_user(self, input_data: BanUserInput, metadata) -> BanUserOutput:
        """Ban a user from the guild."""
        self._validate_snowflake("guild_id", input_data.guild_id)
        self._validate_snowflake("user_id", input_data.user_id)
        
        metadata.log(f"Banning user {input_data.user_id}")
        
        payload = {
            "delete_message_days": input_data.delete_messages_days or 0
        }
        if input_data.reason:
            payload["reason"] = input_data.reason
        
        await self._request(
            "PUT",
            f"/guilds/{input_data.guild_id}/bans/{input_data.user_id}",
            payload
        )
        
        return BanUserOutput(user_id=input_data.user_id, banned=True)
    
    async def unban_user(self, input_data: UnbanUserInput, metadata) -> UnbanUserOutput:
        """Unban a user from the guild."""
        self._validate_snowflake("guild_id", input_data.guild_id)
        self._validate_snowflake("user_id", input_data.user_id)
        
        metadata.log(f"Unbanning user {input_data.user_id}")
        
        await self._request(
            "DELETE",
            f"/guilds/{input_data.guild_id}/bans/{input_data.user_id}"
        )
        
        return UnbanUserOutput(user_id=input_data.user_id, unbanned=True)
    
    async def kick_user(self, input_data: KickUserInput, metadata) -> KickUserOutput:
        """Kick a user from the guild."""
        self._validate_snowflake("guild_id", input_data.guild_id)
        self._validate_snowflake("user_id", input_data.user_id)
        
        metadata.log(f"Kicking user {input_data.user_id}")
        
        endpoint = f"/guilds/{input_data.guild_id}/members/{input_data.user_id}"
        if input_data.reason:
            endpoint += f"?reason={input_data.reason}"
        
        await self._request("DELETE", endpoint)
        
        return KickUserOutput(user_id=input_data.user_id, kicked=True)
    
    # =========================================================================
    # Webhooks
    # =========================================================================
    
    async def create_webhook(self, input_data: CreateWebhookInput, metadata) -> CreateWebhookOutput:
        """Create a webhook in a channel."""
        self._validate_snowflake("channel_id", input_data.channel_id)
        
        metadata.log(f"Creating webhook: {input_data.name}")
        
        result = await self._request(
            "POST",
            f"/channels/{input_data.channel_id}/webhooks",
            {"name": input_data.name}
        )
        
        return CreateWebhookOutput(
            webhook_id=result.get("id", ""),
            name=result.get("name", ""),
            token=result.get("token")
        )
    
    async def execute_webhook(self, input_data: ExecuteWebhookInput, metadata) -> ExecuteWebhookOutput:
        """Execute a webhook to send a message."""
        self._validate_snowflake("webhook_id", input_data.webhook_id)
        
        metadata.log(f"Executing webhook {input_data.webhook_id}")
        
        # For webhooks, we need the token too - this is a limitation
        # In practice, you'd store webhook tokens or use bot API
        raise NotImplementedError(
            "execute_webhook requires a webhook token. "
            "Use Discord bot API for sending messages instead."
        )
