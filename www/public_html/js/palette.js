export function loadPalette() {
 
 // ["#e76254", "#ef8a47", "#f7aa58", "#ffd06f", "#ffe6b7", "#aadce0", "#72bcd5", "#528fad", "#376795", "#1e466e"]
 let palette = {
        "title": "Digital Gender Gap",
        "subtitles": [
            "Less Equality<br><em>female-to-male</em>",
            "More Equality"
        ],
        "colors": [
            "#1e466e",
            "#376795",
            "#528fad",
            "#72bcd5",
            "#aadce0",
            "#ffe6b7",
            "#ffd06f",
            "#f7aa58",
            "#ef8a47",
            "#e76254" 
        ],
        "breaks": {
            "mobile_women": [
                10,
                20,
                30,
                40,
                50,
                60,
                70,
                80,
                90,
                100
            ],
            "mobile_men": [
                10,
                20,
                30,
                40,
                50,
                60,
                70,
                80,
                90,
                100
            ],
            "mobile_fm_ratio": [
                0,
                0.2,
                0.4,
                0.5,
                0.6,
                0.7,
                0.9,
                1.0,
                1.2,
                1.3
            ],
            "internet_women": [
                10,
                20,
                30,
                40,
                50,
                60,
                70,
                80,
                90,
                100
            ],
            "internet_men": [
                10,
                20,
                30,
                40,
                50,
                60,
                70,
                80,
                90,
                100
            ],
            "internet_fm_ratio": [
                0,
                0.1,
                0.3,
                0.4,
                0.5,
                0.6,
                0.7,
                0.8,
                0.9,
                1
            ],
            "mobile_online_offline_model_prediction": [
                10,
                20,
                30,
                40,
                50,
                60,
                70,
                80,
                90,
                100
            ],
            "ground_truth_mobile_gg": [
                10,
                20,
                30,
                40,
                50,
                60,
                70,
                80,
                90,
                100
            ]
}};


    return (palette);
}

