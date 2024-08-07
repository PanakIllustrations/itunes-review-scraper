<?php
header("Access-Control-Allow-Origin: *");

if (isset($_GET['type']) && $_GET['type'] == 'request') {
    $search = $_GET['query'];
    if ($search) {
        $country = ($_GET['country']) ? $_GET['country'] : 'us';
        $url = 'https://www.googleapis.com/books/v1/volumes?q=' . urlencode($search) . '&country=' . $country . '&maxResults=10';
        echo json_encode(["url" => $url]);
        exit;
    }
}

if (isset($_POST['type']) && $_POST['type'] == 'data') {
    $output = array();

    $json = json_decode($_POST['json']);
    
    foreach ($json->items as $item) {
        $data = array();
        $data['title'] = $item->volumeInfo->title;
        $data['authors'] = isset($item->volumeInfo->authors) ? implode(', ', $item->volumeInfo->authors) : 'Unknown';
        $data['publishedDate'] = $item->volumeInfo->publishedDate;
        $data['description'] = $item->volumeInfo->description;
        $data['averageRating'] = isset($item->volumeInfo->averageRating) ? $item->volumeInfo->averageRating : 'No rating';
        $data['ratingsCount'] = isset($item->volumeInfo->ratingsCount) ? $item->volumeInfo->ratingsCount : 'No ratings';
        
        if ($data['title']) {
            $output[] = $data;
        }
    }

    echo json_encode($output);
    exit;
}
?>
