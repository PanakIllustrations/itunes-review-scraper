from flask import Flask, render_template_string, request, jsonify
import requests
import json

app = Flask(__name__)

apiURL = 'https://example.com/api.php'

countries = {
    'ae': 'United Arab Emirates',
    'ag': 'Antigua and Barbuda',
    'ai': 'Anguilla',
    'al': 'Albania',
    'am': 'Armenia',
    'ao': 'Angola',
    'ar': 'Argentina',
    'at': 'Austria',
    'au': 'Australia',
    'az': 'Azerbaijan',
    'bb': 'Barbados',
    'be': 'Belgium',
    'bf': 'Burkina-Faso',
    'bg': 'Bulgaria',
    'bh': 'Bahrain',
    'bj': 'Benin',
    'bm': 'Bermuda',
    'bn': 'Brunei Darussalam',
    'bo': 'Bolivia',
    'br': 'Brazil',
    'bs': 'Bahamas',
    'bt': 'Bhutan',
    'bw': 'Botswana',
    'by': 'Belarus',
    'bz': 'Belize',
    'ca': 'Canada',
    'cg': 'Democratic Republic of the Congo',
    'ch': 'Switzerland',
    'cl': 'Chile',
    'cn': 'China',
    'co': 'Colombia',
    'cr': 'Costa Rica',
    'cv': 'Cape Verde',
    'cy': 'Cyprus',
    'cz': 'Czech Republic',
    'de': 'Germany',
    'dk': 'Denmark',
    'dm': 'Dominica',
    'do': 'Dominican Republic',
    'dz': 'Algeria',
    'ec': 'Ecuador',
    'ee': 'Estonia',
    'eg': 'Egypt',
    'es': 'Spain',
    'fi': 'Finland',
    'fj': 'Fiji',
    'fm': 'Federated States of Micronesia',
    'fr': 'France',
    'gb': 'United Kingdom',
    'gd': 'Grenada',
    'gh': 'Ghana',
    'gm': 'Gambia',
    'gr': 'Greece',
    'gt': 'Guatemala',
    'gw': 'Guinea Bissau',
    'gy': 'Guyana',
    'hk': 'Hong Kong',
    'hn': 'Honduras',
    'hr': 'Croatia',
    'hu': 'Hungary',
    'id': 'Indonesia',
    'ie': 'Ireland',
    'il': 'Israel',
    'in': 'India',
    'is': 'Iceland',
    'it': 'Italy',
    'jm': 'Jamaica',
    'jo': 'Jordan',
    'jp': 'Japan',
    'ke': 'Kenya',
    'kg': 'Krygyzstan',
    'kh': 'Cambodia',
    'kn': 'Saint Kitts and Nevis',
    'kr': 'South Korea',
    'kw': 'Kuwait',
    'ky': 'Cayman Islands',
    'kz': 'Kazakhstan',
    'la': 'Laos',
    'lb': 'Lebanon',
    'lc': 'Saint Lucia',
    'lk': 'Sri Lanka',
    'lr': 'Liberia',
    'lt': 'Lithuania',
    'lu': 'Luxembourg',
    'lv': 'Latvia',
    'md': 'Moldova',
    'mg': 'Madagascar',
    'mk': 'Macedonia',
    'ml': 'Mali',
    'mn': 'Mongolia',
    'mo': 'Macau',
    'mr': 'Mauritania',
    'ms': 'Montserrat',
    'mt': 'Malta',
    'mu': 'Mauritius',
    'mw': 'Malawi',
    'mx': 'Mexico',
    'my': 'Malaysia',
    'mz': 'Mozambique',
    'na': 'Namibia',
    'ne': 'Niger',
    'ng': 'Nigeria',
    'ni': 'Nicaragua',
    'nl': 'Netherlands',
    'np': 'Nepal',
    'no': 'Norway',
    'nz': 'New Zealand',
    'om': 'Oman',
    'pa': 'Panama',
    'pe': 'Peru',
    'pg': 'Papua New Guinea',
    'ph': 'Philippines',
    'pk': 'Pakistan',
    'pl': 'Poland',
    'pt': 'Portugal',
    'pw': 'Palau',
    'py': 'Paraguay',
    'qa': 'Qatar',
    'ro': 'Romania',
    'ru': 'Russia',
    'sa': 'Saudi Arabia',
    'sb': 'Soloman Islands',
    'sc': 'Seychelles',
    'se': 'Sweden',
    'sg': 'Singapore',
    'si': 'Slovenia',
    'sk': 'Slovakia',
    'sl': 'Sierra Leone',
    'sn': 'Senegal',
    'sr': 'Suriname',
    'st': 'Sao Tome e Principe',
    'sv': 'El Salvador',
    'sz': 'Swaziland',
    'tc': 'Turks and Caicos Islands',
    'td': 'Chad',
    'th': 'Thailand',
    'tj': 'Tajikistan',
    'tm': 'Turkmenistan',
    'tn': 'Tunisia',
    'tr': 'Turkey',
    'tt': 'Republic of Trinidad and Tobago',
    'tw': 'Taiwan',
    'tz': 'Tanzania',
    'ua': 'Ukraine',
    'ug': 'Uganda',
    'us': 'United States of America',
    'uy': 'Uruguay',
    'uz': 'Uzbekistan',
    'vc': 'Saint Vincent and the Grenadines',
    've': 'Venezuela',
    'vg': 'British Virgin Islands',
    'vn': 'Vietnam',
    'ye': 'Yemen',
    'za': 'South Africa',
    'zw': 'Zimbabwe'
}
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    entity = request.args.get('entity', 'tvSeason')
    country = request.args.get('country', 'us')

    if not query:
        return jsonify({"error": "No query provided"}), 400

    response = requests.get(apiURL, params={'query': query, 'entity': entity, 'country': country, 'type': 'request'})
    data = response.json()
    
    response = requests.get(data['url'])
    jsonp_data = response.json()
    
    final_response = requests.post(apiURL, data={'json': json.dumps(jsonp_data), 'type': 'data', 'entity': entity})
    final_data = final_response.json()
    
    results_html = ""
    if 'error' in final_data:
        results_html += f"<h3>{final_data['error']}</h3>"
    elif not final_data:
        results_html += "<h3>No results found.</h3>"
    else:
        for result in final_data:
            result_html = f"<div><h3>{result['title']}</h3>"
            if entity not in ['software', 'iPadSoftware', 'macSoftware']:
                uncompressed = result.get('uncompressed')
                hires = result.get('hires')
                result_html += f"<p><a href='{result['url']}' target='_blank'>Standard Resolution</a> | <a href='{uncompressed or hires}' target='_blank'>{'Uncompressed High Resolution' if uncompressed else 'High Resolution'}</a></p>"
            elif entity in ['software', 'iPadSoftware', 'macSoftware']:
                result_html += f"<p><a href='{result['appstore']}' target='_blank'>Application Link</a></p>"
            result_html += "</div>"
            results_html += result_html

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Search Results</title>
    </head>
    <body>
        <a href="/">Go Back</a>
        <div id="results">
            {{ results_html | safe }}
        </div>
    </body>
    </html>
    """, results_html=results_html)

if __name__ == '__main__':
    app.run(debug=True)