from flask import Flask, render_template, request
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

    return render_template('index.html', advisors=advisors.json())

@app.route('/summary')
def summary():
    #  needed headers and cookies for bungie.net API calls
    #  http://www.bungie.net/platform/Destiny/help/
    headers = {'X-API-Key': app.config['API_KEY']}
    cookies = dict(bungledid='B6BGVMQFOKdJsTAWEnsW/ko5xn4glmfRCAAA', bungled='2796665744958383183')

    myUsername = request.args.get('search', '')


    search_url = 'http://www.bungie.net/Platform/Destiny/SearchDestinyPlayer/all/' + myUsername + '/'
    member = requests.get(search_url, headers=headers, cookies=cookies)

    member_id = member.json().get('Response')[0]['membershipId']

    acct_summary_url = 'http://www.bungie.net/Platform/Destiny/1/Account/' + member_id + '/Summary/?definitions=true'
    account = requests.get(acct_summary_url, headers=headers, cookies=cookies)

    #  THIS TAKES FOREVER!!!
    #  FIND A BETTER WAY!!!!
    BUCKET_VAULT_WEAPONS = ''
    BUCKET_VAULT_ARMOR = ''
    BUCKET_VAULT_ITEMS = ''
    #for bucket in account.json()['Response']['definitions']['buckets']:
    #    if account.json()['Response']['definitions']['buckets'][bucket]['bucketIdentifier'] == "BUCKET_VAULT_WEAPONS":
    #        BUCKET_VAULT_WEAPONS = bucket
    #        print "hit 1"
    #        print BUCKET_VAULT_WEAPONS
    #    elif account.json()['Response']['definitions']['buckets'][bucket]['bucketIdentifier'] == "BUCKET_VAULT_ARMOR":
    #        BUCKET_VAULT_ARMOR = bucket
    #        print "hit 2"
    #        print BUCKET_VAULT_ARMOR
    #    elif account.json()['Response']['definitions']['buckets'][bucket]['bucketIdentifier'] == "BUCKET_VAULT_ITEMS":
    #        BUCKET_VAULT_ITEMS = bucket
    #        print "hit 3"
    #        print BUCKET_VAULT_ITEMS


    return render_template('summary.html',
                           account=account.json(),
                           member=member.json(),
                           BUCKET_VAULT_WEAPONS = BUCKET_VAULT_WEAPONS,
                           BUCKET_VAULT_ARMOR = BUCKET_VAULT_ARMOR,
                           BUCKET_VAULT_ITEMS = BUCKET_VAULT_ITEMS)

if __name__ == '__main__':
    app.run(debug=True)
