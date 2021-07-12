#! /usr/bin/env PYTHONIOENCODING=utf8 PYTHONUNBUFFERED=1 /usr/local/bin/python3

# <xbar.title>Nagios</xbar.title>
# <xbar.version>1.0</xbar.version>
# <xbar.author>Samuel Marchal</xbar.author>
# <xbar.author.github>zessx</xbar.author.github>
# <xbar.desc>Monitor Nagios instance.</xbar.desc>
# <xbar.dependencies>python</xbar.dependencies>
# <xbar.abouturl>https://github.com/zessx/xbar-nagios</xbar.abouturl>

# <xbar.var>string(NAGIOS_HOST='https://nagios.example.com'): Nagios host.</xbar.var>
# <xbar.var>string(NAGIOS_USERNAME=''): Nagios username.</xbar.var>
# <xbar.var>string(NAGIOS_PASSWORD=''): Nagios password.</xbar.var>

import re
import requests
import os

NAGIOS_HOST = os.environ.get('NAGIOS_HOST', False)
NAGIOS_USERNAME = os.environ.get('NAGIOS_USERNAME', False)
NAGIOS_PASSWORD = os.environ.get('NAGIOS_PASSWORD', False)

if not NAGIOS_HOST or not NAGIOS_USERNAME or not NAGIOS_PASSWORD:
  print("Nagios: config error | color=purple")

else:
  try:
    data = str(requests.get("%s/cgi-bin/nagios3/tac.cgi" % NAGIOS_HOST, auth=(NAGIOS_USERNAME, NAGIOS_PASSWORD), timeout=1).content)
    
    critical = int(re.search('>(\d+)\sCritical<', data, re.MULTILINE)[1])
    warning = int(re.search('>(\d+)\sWarning<', data, re.MULTILINE)[1])
    unknown = int(re.search('>(\d+)\sUnknown<', data, re.MULTILINE)[1])
    ok = int(re.search('>(\d+)\sOk<', data, re.MULTILINE)[1])
    
    # critical = warning = unknown = ok = 12
    
    services = ok + warning + unknown + critical
    color = 'green'
    if critical > 0:
      color = 'red'
    elif warning > 0 or unknown > 0:
      color = 'yellow'

    output = "%u Ok" % ok
    if services != ok:
      first = True
      if critical > 0:
        output = "{} Cri.".format(critical)
        first = False
      if warning > 0:
        output = ('' if first else output + ' / ') + "{} War.".format(warning)
        first = False
      if unknown > 0:
        output = ('' if first else output + ' / ') + "{} Unk.".format(unknown)

    print("Nagios: {} | color={}".format(output, color))
    print("---")
    print('⚡️ Refresh now | font=Menlo | refresh=true')
    print("⚠️ Show problems | font=Menlo | href={}/cgi-bin/nagios3/status.cgi?host=all&servicestatustypes=28".format(NAGIOS_HOST))
    print("🔎 Show all services | font=Menlo | href={}/cgi-bin/nagios3/status.cgi?host=all".format(NAGIOS_HOST))

  except requests.exceptions.ConnectionError:
    print("Nagios: host unreachable | color=purple")
    
  except Exception as err:
    print("Nagios: {} | color=purple".format(err))
