
var formatAdobeAnalyticsPixel = {

	output: [],
	path: [],
	params: [],
	query: {},
	query_string: '',
	server_call_length: 0,
	no: 1,

	init: function(details) {

		this.setData(details);
		this.setTitle();
		this.setHeader();
		this.setMainBody();
		this.setFooter();
		this.setContextVars();
		this.setAdobeMarketingCloud();
		this.setRecommendations();

		this.printInfo();
	},

	setData: function(details) {
		this.path = details.url.split('/');

		this.params = [];
		this.server_call_length = 0;
		this.query_string = '';

		if(details.method == 'POST' && details.post_query) {
			this.query_string = details.post_query;
			this.server_call_length = (details.url+details.post_query).length;
		} else if(details.url) {
			this.query_string = details.url.split('?')[1] ? details.url.split('?')[1] : '';
			this.server_call_length = details.url.length;
		}

		this.params = this.query_string ? this.query_string.split('&') : [];
		this.query = {};

		for (var k in this.params) {
			if (this.params.hasOwnProperty(k)) {
				var tmp = this.params[k].split('=');
				this.query[tmp[0]] = decodeURIComponent(tmp[1]);
			}
		}
	},

	printInfo: function() {
		console.group(this.output[0]);
		test=[];

		for(var i=1; i<this.output.length; i++) {
			var prefix = this.output[i]['css'] ? '%c' : '';
			var css = this.output[i]['css'] ? this.output[i]['css'] : '';
			if(this.output[i]['info'])
				console.info(prefix + this.output[i]['info'], css)
			else{
                // Gathering analytics data in the test array
				test.push(this.output[i]['line'].replace(':','~~'));
				console.log(prefix + this.output[i]['line'], css)
			}
		}
    
        // Creating CSV formatted data from the analytics data
		// window.open('data:text/csv;charset=utf-8,' + encodeURI(test.join('\n')));
		var encodedURI = 'data:text/csv;charset=utf-8,' + encodeURI(test.join('\n'));
        
        // Creating a temporary link for downloading the encoded CSV data
		var link = document.createElement("a");
		link.setAttribute("href", encodedURI);
		link.setAttribute("download", "adobe-analytics-data-raw.csv");
		link.style.visibility = 'hidden';
		document.body.appendChild(link); // Required for FF

		link.click();

		console.groupEnd();
		this.output = [];
		this.no++;

	},

	setTitle: function() {
		this.output[0] = 'Adobe Analytics Server Call #' + this.no + ' (' + this.server_call_length + ' chars)'
	},

	setHeader: function() {
		if(this.query['pe']) {
		    var types = {
		        'lnk_o': 'CUSTOM LINK',
		        'lnk_e': 'EXIT LINK',
		        'lnk_d': 'DOWNLOAD LINK',
		        'm_i'  : 'MEDIA',
		        'm_s'  : 'MEDIA'
		    }
		    var type = types[this.query['pe']] || 'Unknown';
		    this.output.push({
		        'info': type + Array(20-type.length).join(' ') + ': ' + (this.query['pev2'] || this.query['pev3']),
		        'css': this.css['info']
		    });
		}

		this.output.push({
			'line': 'Report Suite ID    : ' + this.path[5]
		});
	},

	setMainBody: function() {
		for (var k in this.dict) {
			if (this.dict.hasOwnProperty(k)) {
				for(var k1 in this.params) {
					if(this.params.hasOwnProperty(k1)) {
						var param = this.params[k1].split('=');
						if(param[0].match('^'+k+'$')) {
							param[1] = decodeURIComponent(param[1]);
							var value = k=='products' ? this.getProducts(param[1]) : param[1];
							var key = this.dict[k] + (this.dict[k].match(/Hier|eVar|prop/) ? param[0].match(/[0-9]{1,3}/)[0] : '');
							var spaces = key.length > 20 ? 30-key.length : 20-key.length;
							this.output.push({
								'line': key + Array(spaces).join(' ') + ': ' + value,
							});
							delete this.params[k1];
						}
					}
				}
			}
		}
	},

	getProducts: function(products) {

		// dictProducts = {
		// 	0: 'Category   : ',
		// 	1: 'Product    : ',
		// 	2: 'Quantity   : ',
		// 	3: 'Price      : ',
		// 	4: 'Events     : ',
		// 	5: 'eVars      : '
		// }

		// var format = '\n';
		// var products = products.split(',');
		// for (var i=0; i<products.length; i++) {
		// 	format = format + (i==0?'':'\n') + '    #' + (i+1) + '\n';
		// 	item = products[i].split(';');
		// 	for (var y=0; y<item.length; y++) {
		// 		if(item[y]) {
		// 			format += (y <= 5) ? '    ' + dictProducts[y] : '    ';
		// 			format += item[y] + '\n';
		// 		}
		// 	}
		// }

		// return format;
		return products;

	},

	setFooter: function() {
		if(this.query['pe'])
			return;

		var dc = '';
		for (var k in this.dataCenters) {
			if (this.dataCenters.hasOwnProperty(k)) {
				if(this.path[2].match(k)) {
					dc = ' - ' + this.dataCenters[k];
					break;
				}
			}
		}

		var current_domain = location.hostname.split('.');
		var current_subdomain = current_domain.shift();
		var dc_domain = this.path[2].split('.');
		var dc_subdomain = dc_domain.shift();
		var cookies = current_domain.join('.') == dc_domain.join('.') ? 'First-Party' : 'Third-Party';

		if(this.query['j'])
			this.output.push({'line': 'JavaScript Version : ' + this.query['j']});

		this.output.push({'line': 'Version of Code    : ' + this.path[7]});
		this.output.push({'line': 'Data Centre        : ' + this.path[2] + dc});
		this.output.push({'line': 'Cookies            : ' + cookies});
	},

	setContextVars: function() {
		var context = this.query_string.match(/(\&c\.\&)(.*?)(\&\.c\&)/gi) || [];

		if(context.length > 1 || (context.length == 1 && !/activitymap\./.test(context[0])))
			this.output.push({
				'line':'Context Variables',
				'css': this.css['title']
			});

		for (var i=0; i<context.length; i++) {
			var item = context[i].split('&');
			item = item.filter(function(x) {
				return !/^(\.a|a\.|\.c|c\.|\.activitymap)$|^$/.test(x);
			});
			for(var y=0; y<item.length; y++) {
				var tmp = item[y].split('=');
				tmp[1] = tmp[1] ? decodeURIComponent(tmp[1]) : '';
				if(tmp[0] == 'activitymap.')
					this.output.push({
						'line': 'Activity Map',
						'css': this.css['title']
					});
				else
					this.output.push({
						'line': tmp[0] + ': ' + tmp[1]
					});
			}
		}

	},

	setAdobeMarketingCloud: function() {
		if(this.query['pe'])
			return;

		var amc = [];
		if(this.query['mcorgid'])
			amc.push({'line': 'Organisation ID    : ' + this.query['mcorgid'] });
		if(this.query['mid'])
			amc.push({'line': 'Visitor ID         : ' + this.query['mid'] });
		if(this.query['aid'])
			amc.push({'line': 'Legacy Analytics ID: ' + this.query['aid'] });

		if(amc.length > 0) {
			this.output.push({
				'line': 'Adobe Experience Cloud',
				'css': this.css['title']
			});
			this.output = this.output.concat(amc);
		}
	},

	setRecommendations: function() {
		if(this.query['pe'])
			return;

		var rec = [];
		if(/2o7.net/.test(this.path[2]))
			rec.push({'line': this.recommendations['rdc']});
		if(!this.query['mid'])
			rec.push({'line': this.recommendations['visitor']});
		if(!/^JS-/.test(this.path[7]))
			rec.push({'line': this.recommendations['app']});
		if(this.no == 1)
			rec.push({
				'info': this.recommendations['alarmduck'],
				'css': this.css['info']
			});

		if(rec.length>0) {
			this.output.push({
				'line': 'Recommendations',
				'css': this.css['title']
			});
			this.output = this.output.concat(rec);
		}
	},

	css: {
		'body'	: 'all: initial',
		'title'	: 'font-weight: bold',
		'info'	: 'color: blue'
	},

	dict: {
		'pageName'		: 'Page Name',
		'pageType'		: 'Page Type',
		'ch'			: 'Site Section',
		'server'		: 'Server',
		'g'				: 'Current URL',
		'events'		: 'Events',
		'purchaseID'	: 'Purchase ID',
		'products'		: 'Products',
		'xact'			: 'Transaction ID',
		'v0'			: 'Campaign',
		'h([0-9]{1,2})'	: 'Hier',
		'l([0-9]{1,2})'	: 'List eVar',
		'v([0-9]{1,3})'	: 'eVar',
		'c([0-9]{1,3})'	: 'prop',
		'zip'			: 'Zip',
		'tnt'			: 'TnT Campaign',
		'cc'			: 'Currency Code',
		'ce'			: 'Char Set',
		'vid'			: 'Manualy set visitor ID',
	},

	dataCenters: {
		'112.2o7.net' 	  	: 'San Jose, California (non-RDC collection method)',
		'122.2o7.net'		: 'Dallas, Texas (non-RDC collection method)',
		'd1.sc.omtrdc.net'	: 'San Jose, California (RDC)',
		'd2.sc.omtrdc.net'	: 'Dallas, Texas (RDC)',
		'd3.sc.omtrdc.net'	: 'London, United Kingdom (RDC)',
		'sc.omtrdc.net'		: 'Singapore and Pacific Northwest, United States (RDC)'
	},

	recommendations: {
		'rdc'		: 'Migrate to RDC data collection method (https://marketing.adobe.com/resources/help/en_US/whitepapers/rdc/rdc.html)',
		'visitor'	: 'Implement Visitor ID service (https://marketing.adobe.com/resources/help/en_US/mcvid/)',
		'app'		: 'Migrate code library to AppMeasurement (https://marketing.adobe.com/resources/help/en_US/sc/implement/appmeasure_mjs.html)',
		'alarmduck'	: 'Implement automated anomaly detection Slack app (https://www.alarmduck.com/slack?r=ext)'
	}
}

chrome.extension.onMessage.addListener(
	function(request, sender, sendResponse) {
		formatAdobeAnalyticsPixel.init(request);
		return {'cancel': false};
	}
);
