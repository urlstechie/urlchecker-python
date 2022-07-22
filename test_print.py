print("\n\U0001F914 Uh oh... The following urls did not pass:")
file_name = "A-file-name.md"
print(file_name + ":")
url = "https://groups.drupal.org/node/278968"
print(url)
print(" " + url)
print("  " + url)
print("   " + url)
print("    " + url)
print("     " + url)

print()
print("❌️" + url)
print("  ❌️" + url)
print("   ❌️" + url)
print("    ❌️" + url)
print("     ❌️" + url)

print()
print("❌️ " + url)
print("  ❌️ " + url)
print("   ❌️ " + url)
print("    ❌️ " + url)
print("     ❌️ " + url)


print()

def colorize(message):
   print("\033[91m" + message + "\033[0m")


colorize(url)
colorize(" " + url)
colorize("  " + url)
colorize("   " + url)
colorize("    " + url)
colorize("     " + url)

print()
colorize("❌️" + url)
colorize("  ❌️" + url)
colorize("   ❌️" + url)
colorize("    ❌️" + url)
colorize("     ❌️" + url)

print()
colorize("❌️ " + url)
colorize("  ❌️ " + url)
colorize("   ❌️ " + url)
colorize("    ❌️ " + url)
colorize("     ❌️ " + url)
