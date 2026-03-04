# PyPI Release Summary - v0.0.4

## ✅ Successfully Published

### pig-agent-core v0.0.4
- **PyPI URL**: https://pypi.org/project/pig-agent-core/0.0.4/
- **Package Size**:
  - Wheel: 90.9 kB
  - Source: 124.2 kB
- **Upload Time**: 2026-03-04
- **Status**: ✅ Live on PyPI

### pig-coding-agent v0.0.4
- **PyPI URL**: https://pypi.org/project/pig-coding-agent/0.0.4/
- **Package Size**:
  - Wheel: 33.9 kB
  - Source: 36.6 kB
- **Upload Time**: 2026-03-04
- **Status**: ✅ Live on PyPI

## Installation

Users can now install the new versions:

```bash
# Install or upgrade pig-agent-core
pip install --upgrade pig-agent-core

# Install or upgrade pig-coding-agent
pip install --upgrade pig-coding-agent

# Or with uv
uv pip install --upgrade pig-agent-core pig-coding-agent
```

## What's New in v0.0.4

### pig-agent-core
- **Resilience System**: API key rotation with per-failure-type cooldowns
- **Observability System**: Event emission, billing hooks, metrics
- **Context Management**: 3-level compression strategy
- **Memory Protocols**: Pluggable storage backends
- **Enhanced Tool System**: Fallback mapping, confirmation gates
- **330+ new tests**

### pig-coding-agent
- **Resilience Support**: Automatic API key rotation
- **Cost Tracking**: Real-time usage and cost monitoring
- **New Commands**: `/resilience`, `/cost`, `/usage`
- **25 new tests**
- **100% backward compatible**

## Verification

To verify the packages are live:

```bash
# Check pig-agent-core
pip index versions pig-agent-core

# Check pig-coding-agent
pip index versions pig-coding-agent

# Or visit PyPI directly
open https://pypi.org/project/pig-agent-core/
open https://pypi.org/project/pig-coding-agent/
```

## Next Steps

1. ✅ Packages published to PyPI
2. ✅ Documentation updated
3. ✅ CHANGELOG updated
4. 🔄 Merge PR to main branch
5. 🔄 Create GitHub release with release notes
6. 🔄 Announce to users

## Release Notes Template

For GitHub release:

```markdown
# pig-mono v0.0.4 - Production-Ready Resilience & Observability

Major upgrade adding production-ready features to pig-agent-core and pig-coding-agent.

## 🎯 Highlights

- **Automatic API Key Rotation**: Never hit rate limits again
- **Real-time Cost Tracking**: Know exactly what you're spending
- **Production Resilience**: Per-failure-type cooldowns, model fallback
- **Enhanced Observability**: Event emission, metrics, audit logging
- **100% Backward Compatible**: Upgrade without breaking changes

## 📦 Updated Packages

- **pig-agent-core v0.0.4**: Core infrastructure enhancements
- **pig-coding-agent v0.0.4**: Resilience and cost tracking

## 🚀 Installation

```bash
pip install --upgrade pig-agent-core pig-coding-agent
```

## 📖 Documentation

- [CHANGELOG](CHANGELOG.md)
- [pig-agent-core README](packages/pig-agent-core/README.md)
- [pig-coding-agent README](packages/pig-coding-agent/README.md)
- [pig-coding-agent UPGRADE Guide](packages/pig-coding-agent/UPGRADE.md)

## 🙏 Contributors

- @kangkona
- Claude Sonnet 4.6

Full changelog: https://github.com/kangkona/pig-mono/blob/main/CHANGELOG.md
```

## Build Artifacts

Build artifacts are available in:
- `packages/pig-agent-core/dist/`
- `packages/pig-coding-agent/dist/`

These can be used for local testing or distribution.
