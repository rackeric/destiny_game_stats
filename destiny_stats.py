from flask import Flask, render_template, request, redirect, url_for
import requests
import config

app = Flask(__name__)
app.config.from_object(config)

@app.route('/')
def index():
    headers = {'X-API-Key': app.config['API_KEY']}
    cookies = dict(bungledid='B6BGVMQFOKdJsTAWEnsW/ko5xn4glmfRCAAA', bungled='2796665744958383183')

    advisors_url = 'http://www.bungie.net/Platform/Destiny/Advisors/?definitions=true'
    advisors = requests.get(advisors_url, headers=headers, cookies=cookies)

    if advisors.json()['ErrorCode'] is not 1:
        return render_template('error.html', member=advisors.json())

    return render_template('index.html', advisors=advisors.json())

@app.route('/summary')
def summary():
    #  needed headers and cookies for bungie.net API calls
    #  http://www.bungie.net/platform/Destiny/help/
    headers = {'X-API-Key': app.config['API_KEY']}
    cookies = dict(bungledid='B6BGVMQFOKdJsTAWEnsW/ko5xn4glmfRCAAA', bungled='2796665744958383183')

    myUsername = request.args.get('search')

    if not myUsername:
        return redirect(url_for('index'))

    search_url = 'http://www.bungie.net/Platform/Destiny/SearchDestinyPlayer/all/' + myUsername + '/'
    member = requests.get(search_url, headers=headers, cookies=cookies)

    if member.json()['ErrorCode'] is not 1:
        return render_template('error.html', member=member.json())

    member_id = member.json().get('Response')[0]['membershipId']

    acct_summary_url = 'http://www.bungie.net/Platform/Destiny/1/Account/' + member_id + '/Summary/?definitions=true'
    account = requests.get(acct_summary_url, headers=headers, cookies=cookies)

    #if account.json()['ErrorCode'] is 1:
        #  THIS TAKES FOREVER!!!
        #  FIND A BETTER WAY!!!!
        #BUCKET_VAULT_WEAPONS = ''
        #BUCKET_VAULT_ARMOR = ''
        #BUCKET_VAULT_ITEMS = ''
        #for bucket in account.json()['Response']['definitions']['buckets']:
        #    if account.json()['Response']['definitions']['buckets'][bucket].get('bucketIdentifier') == "BUCKET_VAULT_WEAPONS":
        #        BUCKET_VAULT_WEAPONS = bucket
        #        print "hit 1"
        #        print BUCKET_VAULT_WEAPONS
        #    elif account.json()['Response']['definitions']['buckets'][bucket].get('bucketIdentifier') == "BUCKET_VAULT_ARMOR":
        #        BUCKET_VAULT_ARMOR = bucket
        #        print "hit 2"
        #        print BUCKET_VAULT_ARMOR
        #    elif account.json()['Response']['definitions']['buckets'][bucket].get('bucketIdentifier') == "BUCKET_VAULT_ITEMS":
        #        BUCKET_VAULT_ITEMS = bucket
        #        print "hit 3"
        #        print BUCKET_VAULT_ITEMS


    return render_template('summary.html',
                           account=account.json(),
                           member=member.json())
                           #BUCKET_VAULT_WEAPONS = BUCKET_VAULT_WEAPONS,
                           #BUCKET_VAULT_ARMOR = BUCKET_VAULT_ARMOR,
                           #BUCKET_VAULT_ITEMS = BUCKET_VAULT_ITEMS)

if __name__ == '__main__':
    app.run(debug=True)
