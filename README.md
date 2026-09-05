# sys-sdweb title database packer

This small repository converts blawar/titledb's regional JSON into the compact `CFTITLE1` `titles.pack` format consumed by sys-sdweb. The GitHub Action refreshes `US.en.json` daily, on source/workflow changes, or manually, then commits the generated pack and publishes it as an artifact.

Manual corrections go in `overrides.tsv` as `TITLEID<TAB>Name`; overrides always win over upstream data and survive updates. The generated file can be copied to `sdmc:/switch/CyberFoil/offline_db/titles.pack`.

The upstream JSON is large and is used only by CI; the Switch receives the compact binary index. Review upstream licenses and terms before redistributing generated data. No icons or descriptions are included.

Local build:

```sh
curl -LO https://raw.githubusercontent.com/blawar/titledb/master/US.en.json
python3 pack_titles.py US.en.json titles.pack
```
