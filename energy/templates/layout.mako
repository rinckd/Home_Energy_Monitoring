<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <head>
        <script type='text/javascript' src='https://www.google.com/jsapi'></script>
            <script type='text/javascript'>
              google.load('visualization', '1', {'packages':['annotatedtimeline']});
              google.setOnLoadCallback(drawChart);
              function drawChart() {
                var data = new google.visualization.DataTable();
                data.addColumn('datetime', 'Date');
                data.addColumn('number', 'Temperature');
                data.addRows([ ${logging} ]);
                
                var chart = new google.visualization.AnnotatedTimeLine(document.getElementById('chart_div'));
                chart.draw(data, {displayAnnotations: true});
              }
            </script>
        
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
        <title>Home Monitor</title>
        <link rel="shortcut icon" 
              href="${request.static_url('energy:static/favicon.ico')}" />
        <style type="text/css">
              body {
              	font: 100% Verdana, Arial, Helvetica, sans-serif;
              	font-size:12px;
              	color: #333333;
              	background: #333333;
              	margin: 0; 
              	padding: 0;
              	text-align: center; 
              	/* this centers the container in IE 5* browsers. 
              	The text is then set to the left aligned default in the 
              	#container selector */
              	color: #000000;
              }
              .oneColFixCtr #container {
              	width: 1100px;  
              	background:#ffffff;
              	margin: 0 auto; 
              	/* the auto margins (in conjunction with a width) center the page */
              	border: 1px solid #000000;
              	text-align: left; 
              	/* this overrides the text-align: center on the body element. */
              }
              .oneColFixCtr #mainContent {
              	border-bottom: 2px solid #000000;
              	border-top: 2px solid #000000;
              	background:#cccccc;
              	padding: 0 20px;
              }
              .oneColFixCtr #nav {
              	border-top:thick 2px;
              	margin:0;
              	margin-left:200px;
              	padding:0;
              	border-top:2px black;
              }
              .oneColFixCtr #nav li {
              	background: #000000 url(${request.static_url('energy:static/tabs.png')}) 
              	            0 100% no-repeat;
              	list-style:none;
              	float:left;
              	margin:0px;
              	width:${sensor_tabs};
              	/* The width determines the size of the tabs. 
              	This will need to be automated later in Pyramid */
              	white-space:no wrap;
              	line-height: 20px;
              	margin-left:1px;
              	padding-left:5px;
              }
              .oneColFixCtr #nav a {
              	float:none;
              	text-decoration:none;
              	display:block;
              	font-weight:normal;
              	font-size:9px;
               	background: #dddddd url(${request.static_url('energy:static/tabs.png')})
               	            100% 100% no-repeat;
              	color: #ffffcc;
              	padding: 0 0 0 0px;
              }
              .oneColFixCtr #content3 {
              	background:#ffffff;
              	margin-left:auto;
              	margin-right:auto;	
              }
              .oneColFixCtr #nav a:hover {
              	color: #ff0000;
              	border-color:#000000 #cccccc #cccccc #000000;	
              }
              .oneColFixCtr #picked{
                  color: #ff0000;
                  border-color:#000000 #cccccc #cccccc #000000;
                  font-weight:bold;

              }
              div.ui-datepicker{
               font-size:10px;
              }
        </style>
        <!-- These scripts do form calendar, validation and UI elements -->
        <link type="text/css"
         href="${request.static_url(
               'energy:static/jquery/css/dark-hive/jquery-ui-1.8.7.custom.css')}"
               rel="Stylesheet" />
        <script type="text/javascript"
            src="${request.static_url('energy:static/jquery/development-bundle/jquery-1.4.4.js')}">
        </script>
        <script type="text/javascript" 
src="${request.static_url('energy:static/jquery/development-bundle/ui/jquery-ui-1.8.7.custom.js')}">
        </script>	
    </head>

    <body class="oneColFixCtr">
        <div id="container">
            <div id="mainContent">
                <h2>Home Monitor</h2>
            </div>
        <div id = "content2">
            <ul id = "nav">
                <%
                sensor_list = zip(sensors, sensor_links)
                for item_name, item_link in sensor_list:
                    if requestlocation == item_link:
                        context.write("<li><a href='")
                        context.write(changelocation_url)
                        context.write(item_link)
                        context.write("'><div id='picked'>&nbsp;&nbsp;")
                        context.write(item_name)
                        context.write("<br /></div></a></li>")
                    else:
                        context.write("<li><a href='")
                        context.write(changelocation_url)
                        context.write(item_link)
                        context.write("'>")
                        context.write(item_name)
                        context.write('<br /></a></li>')                
                %>
            </ul>
        </div>
        <br />
        <div id = "content3">
            <br />
            <table width="1100" border="0">
                <tr>
                    <td width="300" valign="top" 
                        style="padding:15px;">
                        <div id="cal1Container"></div>
                            <br><br>
                            <div id="datepicker" align="center"></div>
                            <script type="text/javascript">
                                var pickerOpts = {
                                    onSelect: function(date, instance) {
                                        window.location =   
                                        "${request.application_url}"
                                        +"/data/"+date+"/"+"${requestlocation}";
                                        },
                                        defaultDate: new Date ( '${date}' )
                                    }
                                $('#datepicker').datepicker(pickerOpts);
                            </script> 
                        <p><br><br>
                        <a href=https://www.google.com/powermeter>Ted Meter</a>
                    </td>
                    <td width="800">
                        <p><div class="top align-center">
                        <div id='chart_div' style='width: 700px; height: 240px;'></div>
                
                         </div>
                     </td>
                 </tr>
             </table>
         </div>
     </div>    
 </body>
</html>
