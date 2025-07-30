class MsgToEml < Formula
  include Language::Python::Virtualenv

  desc "Convert Microsoft Outlook MSG files to EML format with CLI and GUI"
  homepage "https://github.com/yourusername/msg-to-eml"
  url "https://files.pythonhosted.org/packages/source/m/msg-to-eml/msg-to-eml-1.0.0.tar.gz"
  sha256 "YOUR_SHA256_HASH_HERE"
  license "MIT"

  depends_on "python@3.11"

  resource "extract-msg" do
    url "https://files.pythonhosted.org/packages/source/e/extract-msg/extract_msg-0.47.0.tar.gz"
    sha256 "YOUR_EXTRACT_MSG_SHA256_HERE"
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_match "usage:", shell_output("#{bin}/msg-to-eml --help")

    # Test GUI version exists
    assert_predicate bin/"msg-to-eml-gui", :exist?
  end
end
