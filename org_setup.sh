#!/bin/bash

ORG="gptx-project"  # Change to your GitHub organization
REPOS=(
  "gptx-whitepaper"
  "gptx-info-site"
  "gptx-contracts"
  "gptx-exchange-dapp"
  "gptx-api-backend"
  "gptx-green-ledger"
  "gptx-devops"
  "gptx-community"
)

for REPO in "${REPOS[@]}"; do
  echo "Creating $REPO in org $ORG..."

  # Create GitHub repo
  gh repo create "$ORG/$REPO" --public --confirm

  # Clone it locally
  git clone "https://github.com/$ORG/$REPO.git"
  cd "$REPO" || exit

  # Add a starter README
  cat <<EOF > README.md
# $REPO

This is part of the [GPTX Project](https://gptexchange.info).

> Repository: \`$REPO\`  
> Purpose: _[Add a short description here]_

## License

MIT or Custom License (TBD)
EOF

  git add README.md
  git commit -m "Initial commit for $REPO"
  git push origin main
  cd ..
done

echo "✅ All GPTX repos created and initialized!"
