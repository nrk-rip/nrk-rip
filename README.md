# NRK Rip  [![Build Status](https://travis-ci.org/nrk-rip/nrk-rip.svg?branch=master)](https://travis-ci.org/nrk-rip/nrk-rip)            [![Build Status](https://ci.appveyor.com/api/projects/status/github/nrk-rip/nrk-rip?svg=true)](https://ci.appveyor.com/project/nrk-rip/nrk-rip)

## Dependencies

* Python 3+
* Requests
* FFMPeg (executable placed in same folder as Python script) 

## License

This code is distributed under the MIT License. See [LICENSE.txt](LICENSE.txt) for details.

## Acknowledgments

Script used to convert TTML to SRT is a slightly modified version of the one found in [this repository](https://github.com/nomoketo/ttml2srt).

## Usage

```
python nrk-rip.py <URL> [--quality|-q (high, medium, low)]
```

Example:
 
This retrieves a news program from [NRK TV](https://tv.nrk.no/) and stores it as MKV (with embedded sub if available) in the folder the command is executed from. 

```
python nrk-rip.py https://tv.nrk.no/serie/dagsnytt-atten-tv/NNFA56062117/21-06-2017
```

This retrieves a program from [NRK Radio](https://radio.nrk.no/) and stores it as AAC in the folder the command is executed from.

```
python nrk-rip.py https://radio.nrk.no/serie/popquiz-med-finn-bjelke/MUHR13002217/03-06-2017
```

