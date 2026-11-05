# Modmail Queue
## GitHub Copilot Project Context

## 1. Project Overview

**Modmail Queue** is a public third-party plugin for the Modmail Discord bot.

Its purpose is to introduce a first-come, first-served (FIFO) support ticket queue.

Incoming Modmail tickets are placed into a designated Discord category until a support representative claims them.

Representatives use `?next` to claim the oldest waiting ticket.

Each representative can only have one active ticket assigned to them at a time.

The plugin must operate independently without modifying Modmail's core source code.

---

## 2. Development Environment

| Component | Technology |
|---|---|
| Language | Python |
| Minimum Python version | 3.10 |
| Discord library | discord.py |
| Framework | Modmail plugin system |
| Database | MongoDB |
| Database driver | Motor |
| Repository | GitHub |
| Stable branch | master |
| Development branch | dev |

---

## 3. Modmail Plugin Documentation

The following documentation is based on the official Modmail plugin development documentation supplied for this project.

Treat these requirements as authoritative.

### 3.1 Plugin Requirements

- Support Python 3.10 and above.
- No malicious functionality.
- Do not duplicate functionality pending implementation in Modmail core.
- Modmail core must continue functioning independently.
- Cog names must not conflict with existing classes, including `Core` and `Modmail`.
- Plugin names must not conflict with existing approved plugins.

### 3.2 Plugin Architecture

Modmail plugins use discord.py Cogs.

Basic example:

```python
from discord.ext import commands

class Example(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(Example(bot))
```

### 3.3 Repository Structure

A plugin repository follows this structure:

```text
root/
    plugin_name/
        plugin_name.py
        requirements.txt  # Optional
```

The plugin is loaded using:

```python
await bot.load_extension(
    'username.plugin_name.plugin_name'
)
```

Additional package files, including `__init__.py`, may be included where necessary.

### 3.4 Installing Plugins

Public plugins can be installed using:

```text
?plugin add githubusername/plugin_repo/plugin_name[@branch]
```

The branch parameter is optional and defaults to `master`.

### 3.5 Local Development

Modmail supports local plugins inside:

```text
plugins/@local/
```

A local plugin can be loaded using:

```text
?plugin load @local/plugin_name
```

### 3.6 Database Integration

Plugins must not interact with `bot.api` directly.

Instead, obtain a dedicated MongoDB partition:

```python
def __init__(self, bot):
    self.coll = bot.api.get_plugin_partition(self)
```

The returned collection is a:

```python
motor.motor_asyncio.AsyncIOMotorCollection
```

All database interactions should be asynchronous.

### 3.7 Exposed Modmail Events

Modmail exposes these custom events:

| Event | Parameters |
|---|---|
| `on_plugins_ready` | None |
| `on_thread_initiate` | thread, creator, category, initial_message |
| `on_thread_create` | thread |
| `on_thread_ready` | thread, creator, category, initial_message |
| `on_thread_close` | thread, closer, silent, delete_channel, message, scheduled |
| `on_thread_reply` | thread, from_mod, message, anonymous, plain |

Important guidance:

- `on_thread_ready` is recommended when functionality requires a fully created thread.
- `on_thread_initiate` is generally not recommended.
- `on_thread_close` is dispatched after channel deletion.
- `on_plugins_ready` is dispatched after all plugins have loaded.

Do not assume undocumented behaviour from these events. Inspect Modmail's source code when necessary.

### 3.8 Additional Dependencies

Additional Python dependencies must be declared in:

```text
requirements.txt
```

Avoid unnecessary dependencies.

---

## 4. Product Requirements

### 4.1 Version 1.0.0

The initial release should provide a basic FIFO support ticket queue.

Required functionality:

1. Detect newly created Modmail threads.
2. Automatically add incoming tickets to a queue.
3. Move waiting tickets into a designated Discord category.
4. Display an updating queue-position embed inside each customer's thread.
5. Allow moderators to claim the next ticket using `?next`.
6. Assign tickets exclusively to the claiming moderator.
7. Restrict moderators to one active ticket at a time.
8. Move claimed tickets into a designated active-support category.
9. Update the positions of remaining customers.
10. Persist queue data and assignments in MongoDB.

### 4.2 Queue Behaviour

- Queue ordering must be FIFO (first in, first out).
- The oldest waiting ticket must be assigned first.
- Queue positions start at 1.
- Each moderator can have one active assignment.
- Assignment must be concurrency-safe.
- Customer embeds should be edited rather than repeatedly recreated.
- Queue state must survive bot restarts.
- Closed tickets must not remain in the queue.

### 4.3 Moderator Permissions

Use Modmail's existing moderator permission system wherever possible.

Do not introduce a separate configurable role system in v1.0.0.

Inspect the actual Modmail source code before implementing permission checks.

Do not invent undocumented permission methods.

### 4.4 Customer-Facing Embed

The customer-facing embed should display:

- Queue status.
- Current queue position.
- Number of tickets ahead.
- A short explanation that support will respond when available.

The existing embed should be updated whenever the customer's position changes.

Once assigned, the embed should be removed or updated to indicate that a representative has taken ownership.

---

## 5. Version 1.0.0 Scope Restrictions

The following features are deliberately excluded from the initial release:

- `?my-ticket`
- `?release-ticket`
- `?queue` statistics command
- Administrative configuration commands
- Priority queues
- Estimated waiting times
- Advanced analytics
- Automatic reassignment of representatives

These may be considered for future releases.

Do not implement them prematurely.

---

## 6. Suggested Project Structure

```text
modmail-queue/
│
├── queue/
│   ├── __init__.py
│   ├── queue.py
│   ├── manager.py
│   ├── database.py
│   └── embeds.py
│
├── COPILOT_CONTEXT.md
├── README.md
└── LICENSE
```

Responsibilities:

**queue.py**
- Main Modmail Cog.
- Commands.
- Modmail event listeners.

**manager.py**
- FIFO queue management.
- Ticket assignment.
- Queue operations.

**database.py**
- MongoDB persistence.
- Database operations.

**embeds.py**
- Customer-facing embeds.
- Queue position formatting.

This structure may be adjusted if there is a good technical reason.

---

## 7. Development Standards

GitHub Copilot must follow these rules:

1. Never invent Modmail APIs or undocumented functionality.
2. Inspect the actual Modmail source code when uncertain.
3. Prefer existing Modmail functionality over reimplementing it.
4. Use asynchronous operations where appropriate.
5. Include sensible error handling.
6. Keep the code modular and maintainable.
7. Avoid unnecessary dependencies.
8. Respect the v1.0.0 scope.
9. Ensure database operations are concurrency-safe.
10. Explain significant architectural decisions.
11. Do not modify Modmail core files.
12. Do not implement multiple unrelated features in one change.

If something cannot be verified from the available source code or documentation, explicitly identify the uncertainty instead of guessing.

---

## 8. Development Workflow

- `dev` is the active development branch.
- `master` contains stable releases.
- Test plugins locally using Modmail's `@local` functionality.
- Merge tested changes from `dev` into `master`.
- Maintain versioned releases.
- Update this document when project requirements or architecture change.

---

## 9. Primary Objective

Build a lightweight, reliable and maintainable FIFO support ticket queue that integrates cleanly with Modmail.

The initial release should prioritise reliability and compatibility over feature quantity.

Future releases should expand the plugin incrementally.

---

## 10. Source-Verified Modmail Implementation Findings

The following findings were verified against the Modmail source repository at
`C:\Users\ollie\Documents\modmail-source`. They supplement the official plugin
documentation above. Source behavior may change between Modmail versions, so
implementation must be re-verified when the target Modmail revision changes.

### 10.1 Moderator Permissions

**Verified source behavior:**

- `PermissionLevel.MODERATOR` is defined as level `3` in
  `core/models.py` (`PermissionLevel`).
- `core/checks.py` defines `has_permissions(permission_level)`, which returns a
  `commands.check` predicate.
- The predicate calls `check_permissions(ctx, ctx.command.qualified_name)`.
- Permission evaluation includes bot owners, the bot user, administrators in
  the configured Modmail guild for non-owner commands, explicit command
  permissions, and configured permission levels.
- The check evaluates `ctx.author`, `ctx.author.roles`,
  `ctx.bot.config`, and `ctx.bot.command_perm(...)`. No standalone
  `is_moderator` or `ctx.author.is_mod` API was verified.
- `bot.command_perm(command_name)` resolves a command's required level from
  `override_command_level` or the command check's `permission_level`
  attribute (`bot.py`, `ModmailBot.command_perm`).

**Verified plugin recommendation:**

```python
from core import checks
from core.models import PermissionLevel

@commands.command()
@checks.has_permissions(PermissionLevel.MODERATOR)
async def next(self, ctx):
    ...
```

This follows the existing Modmail Cog pattern, including
`cogs/utility.py` and `cogs/modmail.py`. Do not create a separate configurable
moderator-role system for v1.0.0.

**Source references:**

- `core/checks.py`: `has_permissions`,
  `has_permissions_predicate`, and `check_permissions`
- `core/models.py`: `PermissionLevel`
- `bot.py`: `ModmailBot.command_perm`
- `cogs/utility.py`: the moderator-only `alias` command

### 10.2 Thread Objects and Channels

**Verified source behavior:**

- The concrete class is `core.thread.Thread`.
- Important public properties are `id`, `channel`, `recipient`,
  `recipients`, and `ready`.
- `thread.id` is the primary recipient's Discord user ID. The source does not
  define a separate Modmail-generated thread UUID.
- `thread.recipient` is the primary customer (`discord.User` or
  `discord.Member`); `thread.recipients` includes the primary and additional
  recipients.
- `thread.channel` returns the associated `discord.TextChannel` or
  `discord.DMChannel`; Modmail-created support threads use a text channel.
- Thread channel topics contain `User ID: <recipient.id>`, with optional
  title and additional recipient IDs. `core.utils.parse_channel_topic` parses
  these values.
- `bot.threads.find(channel=channel)` and
  `bot.threads.find(recipient=user)` are the verified thread-manager lookup
  paths. The manager also repopulates its cache from Modmail guild text
  channels at startup.
- The `creator` is passed separately to lifecycle events and `Thread.setup`;
  no public `thread.creator` property was verified.

**Source references:**

- `core/thread.py`: `Thread`, `ThreadManager.find`,
  `ThreadManager.populate_cache`, and `Thread.from_channel`
- `core/utils.py`: `parse_channel_topic` and `create_thread_channel`
- `bot.py`: startup call to `self.threads.populate_cache()`

### 10.3 Thread Lifecycle and Category Movement

**Verified source behavior:**

- `thread_initiate` is dispatched at the start of `Thread.setup`, before
  channel creation; the thread may not have a channel yet.
- `thread_create` is dispatched when `thread.ready` transitions to true.
  This occurs after channel creation and initial log setup, but before the
  final setup tasks and final ready event.
- `thread_ready` is dispatched at the end of `Thread.setup` with
  `thread, creator, category, initial_message`. This is the verified event to
  prefer when a fully initialized thread is required.
- `thread_close` is dispatched after close work completes. If
  `delete_channel=True`, channel deletion is included before dispatch, so
  handlers must not assume the channel still exists.
- `thread_reply` is dispatched after Modmail sends a reply.
- A thread channel is created with
  `bot.modmail_guild.create_text_channel(...)`, including a category,
  permission overwrites, and a topic containing the recipient ID.
- The inspected source moves a channel with Discord.py's
  `await thread.channel.edit(category=target, reason=...)`. No separate
  Modmail category-movement wrapper was verified.

**Recommendation:** For Modmail Queue, listen to `on_thread_ready`, use
`thread.channel`, resolve and validate a `discord.CategoryChannel`, then use
the channel's Discord.py `edit(category=...)` API. Handle missing or deleted
channels explicitly.

**Source references:**

- `core/thread.py`: `Thread.setup`, `Thread.ready`, `Thread.close`,
  and the category edit in the thread-creation-menu flow
- `core/utils.py`: `create_thread_channel`

### 10.4 Plugin Loading, Database, and Lifecycle

**Verified source behavior:**

- Modmail loads an extension with `await bot.load_extension(...)`.
- The extension module is expected to expose:

  ```python
  async def setup(bot):
      await bot.add_cog(PluginCog(bot))
  ```

- Cogs are registered through `await bot.add_cog(...)`.
- Plugins are unloaded with `await bot.unload_extension(...)`. The plugin
  manager also removes the extension's modules from `sys.modules`.
- `bot.api.get_plugin_partition(self)` is implemented by
  `MongoDBClient.get_plugin_partition`. It returns
  `self.db.plugins[cog.__class__.__name__]`.
- `self.db` is an `AsyncIOMotorDatabase`, so the returned value is an
  `AsyncIOMotorCollection`, not a database or custom partition object.
- Isolation is by Cog runtime class name under the MongoDB `plugins`
  collection namespace. This naming is source behavior, not a separately
  verified stable naming contract.
- `bot.plugin_db.get_partition(self)` exists only as a deprecated compatibility
  path. Use `bot.api.get_plugin_partition(self)`.
- Discord.py Cog lifecycle hooks are available; the source demonstrates
  `cog_load` and `cog_unload`.
- Modmail's plugin manager dispatches `plugins_ready` after initial plugin
  loading. No dedicated plugin shutdown event or plugin-specific reload hook
  was verified.
- No installed third-party plugin database example was present in the
  inspected source repository.

**Verified plugin pattern:**

```python
class Queue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.coll = bot.api.get_plugin_partition(self)

async def setup(bot):
    await bot.add_cog(Queue(bot))
```

All collection operations must be asynchronous.

**Source references:**

- `cogs/plugins.py`: plugin path construction, `load_extension`,
  `unload_extension`, `cog_load`, and `plugins_ready`
- `cogs/modmail.py`, `cogs/utility.py`, and `cogs/threadmenu.py`: internal
  `setup(bot)` and Cog registration examples
- `core/clients.py`: `ApiClient.get_plugin_partition`,
  `MongoDBClient.get_plugin_partition`, and deprecated
  `PluginDatabaseClient.get_partition`
- `bot.py`: API client selection and deprecated `plugin_db`

### 10.5 Limitations and APIs Not to Assume

- Do not assume a standalone moderator-status property or undocumented
  permission helper; use `core.checks.has_permissions` with the verified
  `PermissionLevel`.
- Do not assume `thread.id` is a ticket UUID; in the inspected source it is
  the primary customer's Discord user ID.
- Do not assume `thread.creator` exists as a public attribute; use the creator
  event argument where required.
- Do not use `on_thread_initiate` when a channel or fully initialized thread is
  required.
- Do not assume a channel exists during `on_thread_close`; it may already have
  been deleted.
- Do not assume a Modmail wrapper exists for moving categories; the verified
  implementation uses `thread.channel.edit(category=...)`.
- Do not access Modmail's database through `bot.db`, `bot.plugin_db`, or direct
  core database internals for new code. Use the documented
  `bot.api.get_plugin_partition(self)` entry point.
- Do not assume a plugin shutdown event, reload callback, stable collection-name
  contract, or existing third-party database example without verifying the
  target Modmail source.

### 10.6 MongoDB, Motor, and Concurrency Compatibility

The following findings were verified against the inspected Modmail source,
its dependency manifests, and MongoDB/Motor documentation. The MongoDB server
version is not pinned by Modmail and must be verified for each deployment.

**Verified driver versions:**

- `requirements.txt` pins `motor==3.7.1` and `pymongo==4.15.3`.
- `Pipfile` requires Motor `3.7.1` and PyMongo `>=4.9,<5`.
- `Pipfile.lock` locks Motor `3.7.1` and PyMongo `4.15.3`.
- Modmail creates an `AsyncIOMotorClient` and uses the `modmail_bot`
  database. The plugin partition is therefore an asynchronous Motor
  collection.

**Verified database capabilities:**

- Modmail already uses Motor's asynchronous
  `find_one_and_update` in `core/clients.py` for single-document log
  updates. MongoDB documents single-document write operations as atomic,
  including `find_one_and_update`.
- MongoDB supports partial indexes through `partialFilterExpression`.
- MongoDB supports unique partial indexes. The uniqueness constraint applies
  only to documents matching the partial filter, which supports conditional
  uniqueness such as one active assignment per moderator.

**Deployment limitations:**

- Modmail does not check or require a MongoDB server version.
- The Docker deployment uses the unversioned `mongo` image, so the server
  version is deployment-dependent.
- Partial and unique partial indexes require a compatible MongoDB server.
  Verify the actual server version before relying on them; do not infer it
  from the Motor or PyMongo version.
- Unique-index creation can fail when existing data violates the constraint.
  Existing duplicate assignments must be reconciled before creating the
  index.
- Additional restrictions apply if the collection is sharded. The deployment
  must verify whether the plugin collection is sharded and whether the
  desired unique index is permitted.
- Single-document atomicity does not make a sequence of updates across
  multiple ticket documents atomic. Multi-document transactions were not
  established as a Modmail requirement and must not be assumed.

**Recommended concurrency strategy:**

Use a unique partial index together with one atomic claim operation:

```python
await self.coll.create_index(
    [("assigned_to", 1)],
    unique=True,
    partialFilterExpression={
        "status": "assigned",
        "assigned_to": {"$exists": True},
    },
    name="one_assigned_ticket_per_moderator",
)
```

Waiting tickets use `status: "waiting"`. A claim changes the selected oldest
waiting ticket to `status: "assigned"` and sets `assigned_to` and
`assigned_at` in one `find_one_and_update` operation, sorted by the FIFO
timestamp and a deterministic tie-breaker:

```python
ticket = await self.coll.find_one_and_update(
    {"status": "waiting"},
    {
        "$set": {
            "status": "assigned",
            "assigned_to": moderator_id,
            "assigned_at": now,
        }
    },
    sort=[("queued_at", 1), ("_id", 1)],
    return_document=True,
)
```

The exact Motor/PyMongo option spelling must be checked against the installed
driver during implementation. A concurrent claim by the same moderator that
would violate the partial unique index must handle the resulting duplicate-key
error explicitly and report the moderator's existing assigned ticket. Do not
rely only on a preceding read that checks whether the moderator is free; that
check is race-prone.

At plugin startup, verify the MongoDB server version and deployment topology,
reconcile invalid existing assignments, create or verify the unique partial
index, and surface index-creation failures rather than silently continuing.

**Future maintenance:**

Motor's documentation states that Motor is deprecated beginning May 14, 2026,
with critical bug fixes planned until May 14, 2027, and recommends migration
to the PyMongo Async driver. This does not invalidate the currently verified
Modmail dependency, but it is a future maintenance consideration.

**Source and documentation references:**

- `requirements.txt`: pinned Motor and PyMongo versions
- `Pipfile` and `Pipfile.lock`: declared and locked dependency versions
- `core/clients.py`: `AsyncIOMotorClient` construction and
  `find_one_and_update` usage
- `docker-compose.yml`: unversioned MongoDB deployment image
- MongoDB documentation: single-document atomicity and unique partial indexes
- Motor documentation: Motor 3.7.1 requirements and deprecation notice