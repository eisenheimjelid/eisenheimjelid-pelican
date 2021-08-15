Title: Presentando colecciones de MongoDB con Datatables
Date: 2019-06-12 13:00
Category: Php
Tags: mongodb,php,datatables,
Slug: colecciones-de-mongodb-con-datatables
Authors: Joel Rivera
Summary: MongoDB es uno de los manejadores de bases de datos no relacionales (NO-SQL) de más augue actualmente, y con PHP, se hace de una manera sencilla la presentación de ciertos tipos de datos.




Voy a compartir con ustedes, un abstracto de un código que realizó mi conocido [Joel Rivera](https://twitter.com/joel1r "Twitter de Joel Rivera"), para realizar la presentación de colecciones de datos en **MongoDB**, con **PHP** utilizando **Datatables**. Así que manos a la obra.

![MongoDB](/theme/assets/img/mongodb_logo.png)

Empezando por el inicio, el código HTML que va a presentar el Datatables y el contenido de las coleciones de MongoDB, es el siguiente:

### mongodb.html

```html
<!DOCTYPE HTML>
<html>
<head>
    <meta http-equiv="content-type" content="text/html" />
    <title>DataTables mongoDB</title>
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.19/css/jquery.dataTables.min.css">
    <script src="https://code.jquery.com/jquery-3.3.1.js"></script>
    <script src="https://cdn.datatables.net/1.10.19/js/jquery.dataTables.min.js"></script>
</head>

<body>
<p>you can use the file <b>datatables_mongodb.json</b> to load a colection example</p>
<table id="example" class="display" style="width:100%">
        <thead>
            <tr>
                <th>CAMPO 1</th>
                <th>CAMPO 2</th>
                <th>CAMPO 3</th>
                <th>CAMPO 4</th>
                <th>CAMPO 5</th>
            </tr>
        </thead>
    </table>
<script>
$(document).ready(function() {
    $('#example').DataTable( {
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "./server_processing_mongodb.php",
            "dataType": "jsonp",
        },
    //indicate the names of fields how apeart in mongo collection
    "columns": [
            { "data": "campo_1"},
            { "data": "campo_2"},
            { "data": "campo_3"},
            { "data": "campo_4"},
            { "data": "campo_5"}
        ]
});
} );

</script>

</body>
</html>
```

Ahora, el código que realiza el procesamiento de los datos y conecta a MongoDB es el siguiente:

### mongodb.html

```php
<?php
set_time_limit(0);
ini_set('memory_limit', '-1');
error_reporting(E_ALL);
ini_set('display_errors', TRUE);
ini_set('display_startup_errors', TRUE);
date_default_timezone_set('America/Mexico_City');

/**
 * data to modify for it to work
 */
$database   = 'database'; //indicate the name of data base
$collection = 'collection'; //indicate the name of collection
 
/**
 * MongoDB connection
 */
try {
    $m = new MongoDB\Driver\Manager("mongodb://localhost:27017");
} catch (MongoConnectionException $e) {
    die('Error connecting to MongoDB server');
}
/**
 * get the parameters of the call
 */
$input =& $_GET; 
/**
 * get columns
 */
$columnas=[];
foreach($input['columns'] as $cl){
    array_push($columnas,$cl['data']);
}

/**
 * generate custom filter
 */

$condicion=[];
$iColumns = count($input['columns']);
for($i=0;$i<$iColumns;$i++){
    if($input['columns'][$i]['search']['value'] != ""){
        if(is_numeric($input['columns'][$i]['search']['value'])){
           $condicion[$columnas[$i]]= intval($input['columns'][$i]['search']['value']); 
        }else{
            $condicion[$columnas[$i]]= $input['columns'][$i]['search']['value'];
        }        
    }
}

/**
 * search in table
 */
$search = $input['search']['value'];
$base = [];
if($search != ""){
    foreach($columnas as $cl){
        $base[]= [$cl=>['$regex'=>$search]];
    }
    $condicion['$or']=$base;
}
/**
 * order
 */
$sort=[];
if($input['order'][0]['dir']=="asc"){$dir=1;}else{$dir=-1;}
$sort=array($columnas[$input['order'][0]['column']]=>$dir);
/**
 * total results
 */
$total="";
$recordsTotal="";
if(count($condicion)==0){
    $option=array(['$count'=>'total']);
}else{
    $option=array(['$match' => $condicion],['$count'=>'total']);  
}
$command = new MongoDB\Driver\Command([
    'aggregate' => $collection,
    'pipeline' => $option,
    'allowDiskUse' => true,
    'cursor' => new stdClass,
]);
$totales = $m->executeCommand($database, $command);
foreach($totales as $d){
    $total = $d->total;
}
/**
 * Total records in collection
 */
$command = new MongoDB\Driver\Command([
    'aggregate' => $collection,
    'pipeline' => [['$count'=>'total']],
    'allowDiskUse' => true,
    'cursor' => new stdClass,
]);
$totalesx = $m->executeCommand($database, $command);
foreach($totalesx as $d){
   $recordsTotal=$d->total;
}
/**
 * filtering and paging
 */
$project=['_id' => 0];
foreach($columnas as $col){
    $project[$col]=1;
}
if(count($condicion)==0){
    $optionx=array(       
        ['$skip' => intval($input['start'])],
        ['$project'=>$project],             
        ['$limit'=> intval($input['length'])],
        ['$sort'=>$sort],
    );
}else{
    $optionx=array( 
        ['$match'=>$condicion],        
        ['$skip' => intval($input['start'])],
        ['$project'=>$project],            
        ['$limit'=> intval($input['length'])],
        ['$sort'=>$sort], 
          
    );
}
    
$command = new MongoDB\Driver\Command([
    'aggregate' => $collection,
    'pipeline' => $optionx,
    'allowDiskUse' => true,
    'cursor' => new stdClass,
]);
$cursor = $m->executeCommand($database, $command);
/**
 * result
 */

$output = array(
    "draw" => $input['draw'],
    "recordsTotal" => $recordsTotal,
    "recordsFiltered" => $total,
    "data" => array()
);

foreach ( $cursor as $doc ) {
    $finales=array();
    foreach($doc as $key => $value){
        $finales[$key]=$value;
    }
    $output['data'][] = $finales;
}
echo "$input[callback](".json_encode( $output , true),")";
```

Por último, para poder probar este ejemplo, pueden utilizar los [datos de ejemplo](/theme/assets/others/datatables_mongodb.json "Descargar datos de ejemplo JSON"). Es bastante sencillo poder presentar datos desde MongoDB, con ayuda del Datatables y PHP. Espero les sea de ayuda, y cualquier duda o comentario, para eso esta la sección de abajo :D

Saludos y agradecimiento a [Joel Rivera](https://twitter.com/joel1r "Twitter de Joel Rivera") por compartirme su código.

#### Fuentes:

1. [AJAX con Datatables](https://datatables.net/examples/ajax/objects.html "Sitio de Datatables con la documentación para AJAX")
2. [Tutorial de MongoDB](https://docs.mongodb.com/manual/tutorial/ "Documentación de MongoDB")
