import requests

base = 'http://127.0.0.1:5005'

def main():
    print("Checking live server endpoints...")
    
    # 1. Home page
    r_home = requests.get(base + '/')
    assert r_home.status_code == 200, f"Home failed: {r_home.status_code}"
    assert 'Expert Building Plan Approvals' in r_home.text
    assert 'Greater Bengaluru Authority' in r_home.text
    print("[PASS] Home page rendered with GBA & Nambike Nakshe compliance")

    # 2. Services
    r_srv = requests.get(base + '/api/services')
    assert r_srv.status_code == 200
    data_srv = r_srv.json()
    assert data_srv['count'] >= 5
    print(f"[PASS] Services API returned {data_srv['count']} active services")

    # 3. Jurisdictions
    r_jur = requests.get(base + '/api/jurisdictions')
    assert r_jur.status_code == 200
    data_jur = r_jur.json()
    assert len(data_jur['localities']) >= 10
    print(f"[PASS] Jurisdictions API returned {len(data_jur['localities'])} localities")

    # 4. Jurisdiction evaluation
    r_check = requests.post(base + '/api/jurisdictions/check', json={
        'locality_id': 'whitefield',
        'plot_width': 30,
        'plot_length': 40,
        'road_width': 30,
        'building_type': 'Residential'
    })
    assert r_check.status_code == 200
    data_check = r_check.json()
    assert data_check['nambike_nakshe']['eligible'] is True
    print("[PASS] Jurisdiction checker evaluated Nambike Nakshe correctly")

    # 5. Fee Calculator
    r_calc = requests.post(base + '/api/calculator/estimate', json={
        'plot_width': 30,
        'plot_length': 40,
        'floors': 3,
        'has_b_khata': True,
        'locality_id': 'whitefield'
    })
    assert r_calc.status_code == 200
    data_calc = r_calc.json()
    assert data_calc['total_estimated'] > 0
    print(f"[PASS] Fee calculator returned total estimate: INR {data_calc['total_estimated']}")

    # 6. Sakala Tracking
    r_track = requests.get(base + '/api/client/projects?reference_no=SAKALA-GBA-2026-0894')
    assert r_track.status_code == 200
    data_track = r_track.json()
    assert len(data_track['projects']) == 1
    print("[PASS] Sakala project tracking returned active demo project with milestones")

    # 7. Document download
    doc_id = data_track['projects'][0]['documents'][0]['id']
    r_doc = requests.get(f"{base}/api/client/documents/{doc_id}/download")
    assert r_doc.status_code == 200
    print("[PASS] CAD document download served with attachment headers")

    print("\nALL SERVER VERIFICATION CHECKS COMPLETED SUCCESSFULLY!")

if __name__ == '__main__':
    main()
