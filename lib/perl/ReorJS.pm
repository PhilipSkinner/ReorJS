package ReorJS;

use strict;
use warnings;

use LWP::UserAgent;
use JSON qw( from_json );

=pod

=head1 ReorJS.pm - Simple ReorJS Api connector

--
Provides simple programmatic access to the ReorJS server API calls for managing
ReorJS application, dataset and task objects
--
     
Author(s)       - Philip Skinner (philip@crowdca.lc)
Last modified   - 2014-11-01
     
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
        
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
             
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
Copyright (c) 2014, Crowdcalc B.V.
  
<code>
use ReorJS;

my $reorjs = ReorJS->new();
$reorjs->setHost('localhost');
$reorjs->setPort('9999');
$reorjs->setKey('temporary');

my $applications = $reorjs->listApplications();
</code>

=head2 Methods
=cut

=item ReorJS->new()

Creates a new ReorJS API connector object.

Can receive optional hash of parameters. Supported parameters are:

* host
* port
* key
=cut
sub new {
  my ($class, $params) = @_;

  if (!(defined $params)) {
    $params = {};
  }
  
  my $self = {
    host 	=> $params->{host} 	|| 'localhost',
    port 	=> $params->{port} 	|| '9999',
    key 	=> $params->{key} 	|| '',
  };
  
  bless($self, $class);
  
  return $self->_initialize();
}

sub _initialize {
  my $self = shift;
  
  $self->{ua} = LWP::UserAgent->new();
  $self->{ua}->timeout(10);

  return $self;
}

=item $reorjs->setHost($hostname)

Sets the reorjsd hostname to be used for requests
=cut
sub setHost {
  my ($self, $host) = @_;
  
  $self->{host} = $host;
  
  return $self;
}

=item $reorjs->setPort($port)

Sets the port to be used for communication
=cut
sub setPort {
  my ($self, $port) = @_;
  
  $self->{port} = $port;
  
  return $self;
}

=item $reorjs->setKey($key)

Sets the access key to be used for authentication
=cut
sub setKey {
  my ($self, $key) = @_;
  
  $self->{key} = $key;
  
  return $self;
}

=item $reorjs->detailTask($id)

Returns details for a particular task in the system
=cut
sub detailTask {
  my ($self, $id) = @_;
  my $response = $self->{ua}->get($self->_generateURL('/api/v1/task/' . $id . '?key=' . $self->{key}));
  
  if ($response->is_success) {
    return $self->_checkData(from_json($response->decoded_content));
  } else {
    die $response->status_line;
  }
}

=item $reorjs->createTask($params)

Creates a task in the system

Receives a hash of parameters. Supported parameters are:

* application
* dataset
* result
=cut
sub createTask {
  my ($self, $params) = @_;
  my $response = $self->{ua}->post($self->_generateURL('/api/v1/application'),
                                    Content => {
                                      key 		=> $self->{key},
                                      application 	=> $params->{application},
                                      dataset 		=> $params->{dataset},
                                      result 		=> $params->{result},
                                    });
  
  if ($response->is_success) {
    return $self->_checkData(from_json($response->decoded_content));
  } else {
    die $response->status_line;
  }  
}

=item $reorjs->listTasks()

Lists all of the tasks currently in the system
=cut
sub listTasks {
  my ($self) = @_;
  my $response = $self->{ua}->get($self->_generateURL('/api/v1/task?key=' . $self->{key}));
  
  if ($response->is_success) {
    return $self->_checkData(from_json($response->decoded_content));
  } else {
    die $response->status_line;
  }
}

=item $reorjs->createDataset($params)

Creates a new dataset (or source) in the system

Receives a hash of parameters. Supported parameters are:

* name
* source_type
* source_hostname
* source_port
* source_name
* source_table
* source_username
* source_password
=cut
sub createDataset {
  my ($self, $params) = @_;
  my $response = $self->{ua}->post($self->_generateURL('/api/v1/dataset'),
                                    Content => {
                                      key 		=> $self->{key},
                                      name 		=> $params->{name},
                                      source_type 	=> $params->{source_type},
                                      source_hostname 	=> $params->{source_hostname},
                                      source_port 	=> $params->{source_port},
                                      source_name 	=> $params->{source_name},
                                      source_table 	=> $params->{source_table},
                                      source_username 	=> $params->{source_username},
                                      source_password 	=> $params->{source_password},
                                    });
  
  if ($response->is_success) {
    return $self->_checkData(from_json($response->decoded_content));
  } else {
    die $response->status_line;
  }  
}

=item $reorjs->modifyDataset($id, $params)

Modifies an existing dataset

Receives a hash of parameters. Supported parameters are:

* name
* source_type
* source_hostname
* source_port
* source_name
* source_table
* source_username
* source_password
=cut
sub modifyDataset {
  my ($self, $id, $params) = @_;
  my $response = $self->{ua}->post($self->_generateURL('/api/v1/dataset/' . $id),
                                    Content => {
                                      key 		=> $self->{key},
                                      name 		=> $params->{name},
                                      source_type 	=> $params->{source_type},
                                      source_hostname	=> $params->{source_hostname},
                                      source_port 	=> $params->{source_port},
                                      source_name 	=> $params->{source_name},
                                      source_table 	=> $params->{source_table},
                                      source_username 	=> $params->{source_username},
                                      source_password 	=> $params->{source_password},
                                    });
  
  if ($response->is_success) {
    return $self->_checkData(from_json($response->decoded_content));
  } else {
    die $response->status_line;
  }  
}

=item $reorjs->deleteDataset($id)

Deletes a dataset
=cut
sub deleteDataset {
  my ($self, $id) = @_;
  my $response = $self->{ua}->delete($self->_generateURL('/api/v1/dataset/' . $id . '?key=' . $self->{key}));
  
  if ($response->is_success) {
    return $self->_checkData(from_json($response->decoded_content));
  } else {
    die $response->status_line;
  }
}

=item $reorjs->detailDataset($id)

Returns the details for a dataset
=cut
sub detailDataset {
  my ($self, $id) = @_;
  my $response = $self->{ua}->get($self->_generateURL('/api/v1/dataset/' . $id . '?key=' . $self->{key}));
  
  if ($response->is_success) {
    return $self->_checkData(from_json($response->decoded_content));
  } else {
    die $response->status_line;
  }
}

=item $reorjs->listDatasets($params)

Returns a list of datasets in the system
=cut
sub listDatasets {
  my ($self) = @_;
  my $response = $self->{ua}->get($self->_generateURL('/api/v1/dataset?key=' . $self->{key}));
  
  if ($response->is_success) {
    return $self->_checkData(from_json($response->decoded_content));
  } else {
    die $response->status_line;
  }
}

=item $reorjs->createApplication($params)

Creates a new application

Receives a hash of parameters. Supported parameters are:

* name
* program
=cut
sub createApplication {
  my ($self, $params) = @_;
  my $response = $self->{ua}->post($self->_generateURL('/api/v1/application'),
                                    Content => {
                                      key 		=> $self->{key},
                                      name 		=> $params->{name},
                                      program 		=> $params->{program}
                                    });
  
  if ($response->is_success) {
    return $self->_checkData(from_json($response->decoded_content));
  } else {
    die $response->status_line;
  }  
}

=item $reorjs->modifyApplication($id, $params)

Modifies an application

Receives a hash of parameters. Supported parameters are:

* name
* program
=cut
sub modifyApplication {
  my ($self, $id, $params) = @_;
  my $response = $self->{ua}->post($self->_generateURL('/api/v1/application/' . $id),
                                    Content => {
                                      key 		=> $self->{key},
                                      name 		=> $params->{name},
                                      program 		=> $params->{program}
                                    });
  
  if ($response->is_success) {
    return $self->_checkData(from_json($response->decoded_content));
  } else {
    die $response->status_line;
  }  
}

=item $reorjs->deleteApplication($id)

Deletes an application
=cut
sub deleteApplication {
  my ($self, $id) = @_;
  my $response = $self->{ua}->delete($self->_generateURL('/api/v1/application/' . $id . '?key=' . $self->{key}));
  
  if ($response->is_success) {
    return $self->_checkData(from_json($response->decoded_content));
  } else {
    die $response->status_line;
  }
}

=item $reorjs->listApplications($params)

Lists all of the applications
=cut
sub listApplications {
  my ($self) = @_;
  my $response = $self->{ua}->get($self->_generateURL('/api/v1/application?key=' . $self->{key}));
  
  if ($response->is_success) {
    return $self->_checkData(from_json($response->decoded_content));
  } else {
    die $response->status_line;
  }
}

#private methods#

sub _checkData {
  my ($self, $data) = @_;
  if (defined $data->{meta}) {
    if (defined $data->{meta}{code} && $data->{meta}{code} eq '200') {
      if (defined $data->{data}) {
        return $data->{data};
      } elsif (defined $data->{status}) {
        return $data;
      }
    } else {
      if (defined $data->{error}) {
        return {
          error => $data->{error},
          code => $data->{meta}{code},
        };
      }
    }
  }
  
  return {};
}

sub _generateURL {
  my ($self, $endpoint) = @_;  
  return 'http://' . $self->{host} . ':' . $self->{port} . $endpoint;
}

return 1;
