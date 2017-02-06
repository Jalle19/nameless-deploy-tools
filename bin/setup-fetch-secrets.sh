#!/bin/bash

# Copyright 2017 Nitor Creations Oy
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit 1
fi
if ! [[ "$1" =~ ^lpass$|^s3$|^vault$ ]]; then
  echo "usage: $0 <lpass|s3|vault>"
  exit 1
fi

if [ "$1" = "lpass" ]; then
  source $(n-include common_tools.sh)
  ln -snf $(n-include lpass_$(system_type_and_version)) /usr/bin/lpass
fi
ln -snf $(n-include fetch-secrets-$1.sh) /usr/bin/fetch-secrets.sh
ln -snf $(n-include store-secret-$1.sh) /usr/bin/store-secret.sh