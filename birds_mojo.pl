#! /usr/bin/env perl
#
# Bird classification deployment app with fastai2
# Front end with vuejs
# Back end with Mojolicious and python starlette
#
# Sylvain Thibault April 20
#
use Mojolicious::Lite -signatures, -async_await;

# local URL for predictions from URL to python service
my $surl = 'http://localhost:8008/classify-url';

# local URL for predictions from file upload to python service
my $burl = 'http://localhost:8008/uploadb';

app->secrets(['fastai2 rocks, so does mojolicious']);

# app bound to port 8010
app->config(hypnotoad => {listen => ['http://*:8010']}, proxy => 1);

get 'bird_name' => async sub($c) {
  $c->app->log->info(
    "Service accessed from " . $c->req->headers->header('X-Forwarded-For'));

  # get vocab data from model
  my $vocab = await($c->ua->get_p('http://localhost:8008/vocab'))->res->json;
  my @cat   = map { lc $_ } $vocab->{vocab}->@*;

  # pass to template
  $c->stash(birds => \@cat);
  $c->render('index');
};

# image from url
post 'from_url' => async sub($c) {
  $c->render_later;
  my $data = $c->req->json;
  $c->app->log->debug($data->{'imageUrl'});

  # query python service
  my $json
    = await($c->ua->post_p($surl => json => {url => $data->{'imageUrl'}}))
    ->res->json;

  # use first 5 results
  @{$json->{predictions}} = splice(@{$json->{predictions}}, 0, 5);
  $c->render(json => $json);
};

# upload image
post 'upload' => async sub($c) {
  $c->render_later;

  # Check file size
  return $c->render(text => 'File is too big.', status => 200)
    if $c->req->is_limit_exceeded;
  my $file = $c->param('target');

  # query python service with byte payload
  my $json
    = await(
    $c->ua->post_p($burl => {'Content-Type' => 'image/jpeg'}, $file->slurp))
    ->res->json;

  # use first 5 results
  @{$json->{predictions}} = splice(@{$json->{predictions}}, 0, 5);
  $c->render(json => $json);
};


app->start;
