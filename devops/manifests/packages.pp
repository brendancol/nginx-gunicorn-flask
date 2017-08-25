class packages {

  package { "python27":
    ensure => present,
  }
  package { "python27-devel":
    ensure => present,
  }
  package { "nginx":
    ensure => present,
  }
  package { "postgresql96-server":
    ensure => present,
  }
  package { "libssl-dev":
    ensure => present,
  }

}

include packages