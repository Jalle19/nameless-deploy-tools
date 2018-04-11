#!/bin/bash -x

# Copyright 2016 Nitor Creations Oy
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

VERSION=$(grep version setup.py | cut -d\' -f 2)
MAJOR=${VERSION//.*}
MINOR=${VERSION##*.}
if [ "$1" = "-m" ]; then
  MAJOR=$(($MAJOR + 1))
  MINOR="0"
  NEW_VERSION=$MAJOR.$MINOR
  shift
elif [ "$1" = "-v" ]; then
  shift
  NEW_VERSION="$1"
  shift
else
  MINOR=$(($MINOR + 1))
  NEW_VERSION=$MAJOR.$MINOR
fi

sed -i "s/$VERSION/$NEW_VERSION/g" setup.py
./update-readme.sh
sed -i "s/## Released version.*/## Released version $NEW_VERSION/g" README.md
sed -i "s/nitor-deploy-tools==.*/nitor-deploy-tools==$NEW_VERSION/g" docker/Dockerfile
git commit -m "$1" setup.py README.md docker/Dockerfiles
git tag "$NEW_VERSION" -m "$1"
git push --tags origin master

python setup.py register -r pypi
python setup.py sdist upload -r pypi --sign
docker build -t ndt docker
docker login -u "$(git config docker.username)" -p "$(lpass show --password docker.com)"
docker tag ndt:latest nitor/ndt:$NEW_VERSION
docker push nitor/ndt:$NEW_VERSION