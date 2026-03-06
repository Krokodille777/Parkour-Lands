# tools at your disposal

## WSL2 and Python 3.12

You have access to a WSL2 environment with Python 3.12 installed. You can use this environment to run Python scripts, install packages, and perform various tasks.

## Context7 MCP

Context7 is a MCP server you can use to look up docs for libraries, frameworks, etc. Actively use it to make sure you have access to latest APIs and to get code examples. You can ask it questions about how to use certain libraries or functions, and it will provide you with relevant documentation and examples.

## Web search

When you don't need to explicitly search docs only, or when Context7 doesn't yield appropriate results, you can use the web search tool to find information on the internet. This can be useful for finding tutorials, blog posts, or other resources that may not be available in the official documentation.

## AdvFS MCP

You have a built-in set of tools, but it's severely limited when reading files, particularly because of the 256-line/10KB limit for reading. It's recommended to read files in whole as there is a lot of important context that you will otherwise miss if you read them in parts, and AdvFS MCP allows you to do that - it doesn't have this limit.

So, it's recommended:

1. Use AdvFS MCP to read files in whole, even if they are large. This will ensure you have all the necessary context and information from the file.
2. For searching and reading in parts, your built-in tools might be better, but AdvFS can also work for larger sections thanks to customizable parameters.
3. For writing and editing, your built-in tools are unmatched, so use them for any modifications you need to make to files.
4. Any additional commands (via `bash`) that you might need to run can be executed using your built-in tools as well.