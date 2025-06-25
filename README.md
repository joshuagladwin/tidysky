# TidySky

[![.github/workflows/actions.yml](https://github.com/joshuagladwin/tidysky/actions/workflows/actions.yml/badge.svg)](https://github.com/joshuagladwin/tidysky/actions/workflows/actions.yml)

Python script to delete old likes and posts from your BSky account.

Runs as a daily cron-job scheduled Github Action, deleting likes and posts older than `DELETE_DAYS_OLDER`.

※ This just deletes likes/posts - doesn't save/archive before deletion. 

## Set-Up

To run as a Github action, set the following as Repository Secrets:

* `<USERNAME>` e.g `example.bsky.social`
* `<PASSWORD>` e.g `password1234`
* `<DELETE_DAYS_OLD>` e.g `7`
