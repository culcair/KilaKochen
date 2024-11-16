def test_home_route(client):
    response = client.get("/week")
    assert (
        b"Wochenplan" in response.data
    )  # Beispiel für den erwarteten Text auf der Seite
