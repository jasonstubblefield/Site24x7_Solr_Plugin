# Site24x7 Solr Monitor

Site24x7 is a popular infrastructure monitoring solution that has the ability to use custom plugins.

There are many plugins that come included with Site24x7 but Solr is not one of them.

Here is a Solr plugin for Site24x7 that will provide basic monitoring capabilities.

## How to use

Make a folder in the site 24x7 plugin folder, usually at `/opt/site24x7` on your server: 

`/opt/site24x7/monagent/plugins/solr_monitor`

Copy the `solr_monitor.py` script to the folder created above, please note, the folder name and the script name must be the same for the plugin to work:

`/opt/site24x7/monagent/plugins/solr_monitor/solr_monitor.py`

Site 24x7 should detect the plugin automatically.

Please change the version number in whole integers only if you modify this script and site24x7 will pick up the changes automatically when it detects the new version number.

