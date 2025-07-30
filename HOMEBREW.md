# Homebrew Installation Guide

This guide explains how to prepare and publish `msg-to-eml` to Homebrew.

## Prerequisites

1. **GitHub Repository**: Your code should be in a public GitHub repository
2. **Release**: Create a tagged release on GitHub
3. **Homebrew Tap**: Either submit to main Homebrew or create your own tap

## Step 1: Prepare for Release

1. **Update version** in `pyproject.toml`:

   ```toml
   version = "1.0.0"
   ```

2. **Build and test the package**:

   ```bash
   ./scripts/build.sh
   ```

3. **Create a GitHub release**:
   - Tag version: `v1.0.0`
   - Upload the source tarball from `dist/msg-to-eml-1.0.0.tar.gz`

## Step 2: Get Package Information

1. **Calculate SHA256** of your release tarball:

   ```bash
   curl -sL https://github.com/USERNAME/msg-to-eml/archive/v1.0.0.tar.gz | shasum -a 256
   ```

2. **Get dependency SHA256s**:
   ```bash
   # For extract-msg
   pip download extract-msg==0.47.0 --no-deps
   shasum -a 256 extract_msg-0.47.0.tar.gz
   ```

## Step 3: Create Homebrew Formula

Update the formula in `homebrew/msg-to-eml.rb`:

```ruby
class MsgToEml < Formula
  include Language::Python::Virtualenv

  desc "Convert Microsoft Outlook MSG files to EML format with CLI and GUI"
  homepage "https://github.com/USERNAME/msg-to-eml"
  url "https://github.com/USERNAME/msg-to-eml/archive/v1.0.0.tar.gz"
  sha256 "YOUR_ACTUAL_SHA256_HERE"
  license "MIT"

  depends_on "python@3.11"

  resource "extract-msg" do
    url "https://files.pythonhosted.org/packages/source/e/extract-msg/extract_msg-0.47.0.tar.gz"
    sha256 "EXTRACT_MSG_SHA256_HERE"
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_match "usage:", shell_output("#{bin}/msg-to-eml --help")
    assert_predicate bin/"msg-to-eml-gui", :exist?
  end
end
```

## Step 4: Submit to Homebrew

### Option A: Main Homebrew Repository

1. Fork the [Homebrew/homebrew-core](https://github.com/Homebrew/homebrew-core) repository
2. Add your formula to `Formula/msg-to-eml.rb`
3. Submit a pull request

### Option B: Personal Tap (Easier)

1. Create a repository named `homebrew-tools` (or similar)
2. Add your formula as `Formula/msg-to-eml.rb`
3. Users install with:
   ```bash
   brew tap USERNAME/tools
   brew install msg-to-eml
   ```

## Step 5: Test the Formula

```bash
# Test installation locally
brew install --build-from-source --verbose --debug homebrew/core/msg-to-eml

# Test the CLI
msg-to-eml --help

# Test the GUI
msg-to-eml-gui
```

## Usage After Installation

Once installed via Homebrew, users can:

```bash
# CLI usage
msg-to-eml input.msg output.eml
msg-to-eml folder/ --batch --next-to-original

# GUI usage
msg-to-eml-gui
```

## Notes

- The formula installs both CLI (`msg-to-eml`, `msg2eml`) and GUI (`msg-to-eml-gui`) commands
- Dependencies are automatically managed by the virtualenv
- macOS users get a native experience with proper integration
