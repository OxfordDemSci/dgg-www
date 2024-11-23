def test_init(session, test_client, app, db):
    response = test_client.get("/api/v2/init")
    assert response.status_code == 200
    assert {'iso3code': 'ALB', 'country': 'Albania'} in response.json["national"]["countries"]
    assert "internet_men" in response.json["national"]["models"]
    assert "internet_men" in response.json["subnational"]["models"]
    assert "2024-06" in response.json["national"]["dates"]
    assert "2024-06" in response.json["subnational"]["dates"]


def test_query_specific_country_valid(session, test_client, app, db):
    response = test_client.get('/api/v2/query_specific_country?country=ALB')
    assert response.status_code == 200
    data = response.get_json()
    assert "ALB" in data
    assert "2024-05" in data["ALB"]
    assert "internet_fm_ratio" in data["ALB"]["2024-05"]
    assert data["ALB"]["2024-05"]["internet_fm_ratio"]["predicted"] == 0.998
    assert data["ALB"]["2024-05"]["internet_fm_ratio"]["predicted_error"] == 0.146
    print("ALL DONE TESTING")


def test_query_spcific_country_invalid(session, test_client, app, db):
    response = test_client.get('/api/v2/query_specific_country?country=XXX')
    assert response.status_code == 400
    assert response.json["error"] == "Invalid country - XXX"


def test_query_specific_region_valid(session, test_client, app, db):
    response = test_client.get('/api/v2/query_specific_region?region=ALB.1_1')
    assert response.status_code == 200
    data = response.get_json()
    assert "ALB.1_1" in data
    assert "2024-05" in data["ALB.1_1"]
    assert "internet_fm_ratio" in data["ALB.1_1"]["2024-05"]
    assert data["ALB.1_1"]["2024-05"]["internet_fm_ratio"]["predicted"] == 1
    assert data["ALB.1_1"]["2024-05"]["internet_fm_ratio"]["predicted_error"] == 0.145


def test_query_specific_region_invalid(session, test_client, app, db):
    response = test_client.get('/api/v2/query_specific_region?region=XXX')
    assert response.status_code == 400
    assert response.json["error"] == "Invalid region - XXX"


def test_get_national_data_valid(session, test_client, app, db):
    response = test_client.get('/api/v2/get_national_data?date=2024-05')
    assert response.status_code == 200
    data = response.get_json()
    assert "ALB" in data
    assert "internet_fm_ratio" in data["ALB"]
    assert data["ALB"]["internet_fm_ratio"]["predicted"] == 0.998
    assert data["ALB"]["internet_fm_ratio"]["predicted_error"] == 0.146


def test_get_national_data_invalid(session, test_client, app, db):
    response = test_client.get('/api/v2/get_national_data?date=1935-06')
    assert response.status_code == 400
    assert response.json["error"] == "Invalid date 1935-06"


def test_get_subnational_data_valid(session, test_client, app, db):
    response = test_client.get('/api/v2/get_subnational_data?date=2024-05')
    assert response.status_code == 200
    data = response.get_json()
    assert "ALB.1_1" in data["ALB"]
    assert "internet_fm_ratio" in data["ALB"]["ALB.1_1"]
    assert data["ALB"]["ALB.1_1"]["internet_fm_ratio"]["predicted"] == 1
    assert data["ALB"]["ALB.1_1"]["internet_fm_ratio"]["predicted_error"] == 0.145


def test_get_subnational_data_invalid(session, test_client, app, db):
    response = test_client.get('/api/v2/get_subnational_data?date=1935-06')
    assert response.status_code == 400
    assert response.json["error"] == "Invalid date 1935-06"


def test_get_ground_truth_national(session, test_client, app, db):
    response = test_client.get('/api/v2/get_ground_truth_national')
    assert response.status_code == 200
    data = response.get_json()
    assert "ALB" in data
    assert data["ALB"]["mobile_women"] == 90.1


def test_get_ground_truth_subnational(session, test_client, app, db):
    response = test_client.get('/api/v2/get_ground_truth_subnational')
    assert response.status_code == 200
    data = response.get_json()
    assert "ALB.1_1" in data["ALB"]
    assert "mobile_women" in data["ALB"]["ALB.1_1"]
    assert data["ALB"]["ALB.1_1"]["mobile_women"] == 84.4


def test_download_csv_national(session, test_client, app, db):
    response = test_client.get('/api/v2/download_csv?level=national&start_date=2024-05&end_date=2024-07')
    assert response.status_code == 200
    assert response.headers["Content-Disposition"] == "attachment; filename=national_data_2024-05_to_2024-07.csv"
    assert response.headers["Content-Type"] == "text/csv"
    assert response.headers["Content-Length"] > "0"


def test_download_csv_subnational(session, test_client, app, db):
    response = test_client.get('/api/v2/download_csv?level=subnational&start_date=2024-05&end_date=2024-07')
    assert response.status_code == 200
    assert response.headers["Content-Disposition"] == "attachment; filename=subnational_data_2024-05_to_2024-07.csv"
    assert response.headers["Content-Type"] == "text/csv"
    assert response.headers["Content-Length"] > "0"
  
