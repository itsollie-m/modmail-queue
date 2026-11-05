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