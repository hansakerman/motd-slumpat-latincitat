#!/usr/bin/env bash
#
# slumpat_citat.sh
#
# Skriver ut ett slumpmässigt latinskt citat med svensk översättning
# från latin_citat_normaliserat.txt. Fungerar i både bash och zsh.
#
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
citat_fil="${script_dir}/latin_citat_normaliserat.txt"

if [[ ! -f "$citat_fil" ]]; then
    echo "Hittar inte citatfilen: $citat_fil" >&2
    exit 1
fi

rad="$(awk -v seed="$RANDOM$$" 'BEGIN{srand(seed)} {a[NR]=$0} END{print a[int(rand()*NR)+1]}' "$citat_fil")"

citat="${rad%%|*}"
oversattning="${rad#*|}"

printf '%s\n  — %s\n' "$citat" "$oversattning"
