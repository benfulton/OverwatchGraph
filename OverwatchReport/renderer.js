// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// All of the Node.js APIs are available in this process.
const Highcharts = require('highcharts');
const $ = require("jquery");
const mysql      = require('mysql');

function per_ten_minutes(general, datapoint) {
    const translate = new Map([['Damage', 'hero_damage_done'],
        ['Cards', 'cards'],
    ['Deaths', 'deaths'],
        ['Eliminations', 'eliminations'],
        ['Medals', 'medals'],
        ['Objective Kills', 'objective_kills'],
        ['Objective Time', 'objective_time'],
        ['Wins', 'games_won']]);
    const value = general[translate.get(datapoint)];
    const ten_minutes = general['time_played'] * 6;
    return value/ten_minutes;
}

function highchartize(rows, hero, stat)
{
    return rows.map(function(e) {
        let val = null;
        try {
            const j = JSON.parse(e['json']);
            val = per_ten_minutes(j.heroes.stats.quickplay[hero].general_stats, stat);
        }
        catch (e) {

        }
        const dt = e['created_at'];
        return [Date.UTC(dt.getFullYear(), dt.getMonth(), dt.getDate()), val];
    });
}

const info = {
    host     : 'localhost',
    user     : 'overwatch',
    password : 'pharmercy',
    database : 'overwatch'
};

function update_chart(hero, stat) {
    var connection;
    connection = mysql.createConnection(info);

    connection.connect();

    connection.query("SELECT created_at, json FROM overwatch.statistics where battletag like 'syz%' order by created_at", function (error, results, fields) {
        if (error) throw error;
        values = highchartize(results, hero, stat);

        Highcharts.chart('container', {

            title: {
                text: hero
            },

            xAxis: {
                type: 'datetime'
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle'
            },

            plotOptions: {
                series: {
                    label: {
                        connectorAllowed: false
                    }
                }
            },

            series: [{
                data: values,
                name: stat
            }],

            responsive: {
                rules: [{
                    condition: {
                        maxWidth: 500
                    },
                    chartOptions: {
                        legend: {
                            layout: 'horizontal',
                            align: 'center',
                            verticalAlign: 'bottom'
                        }
                    }
                }]
            }

        });

    });

    connection.end();
}

$( "#hero" ).change(function() {
    update_chart($( this ).val(), $( '#stat' ).val());
});

$( "#stat" ).change(function() {
    update_chart($( "#hero" ).val(), $( this ).val());
});

update_chart($( "#hero" ).val(), $( '#stat' ).val())
