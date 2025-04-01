from gtrending import fetch_repos

# Fetch trending Python repositories for today
repos = fetch_repos(language="ruby", since="daily")

# Print repository details
for i, repo in enumerate(repos, 1):
    print(f"{i}. {repo['fullname']} - {repo['description']} (Stars: {repo['stars']})")