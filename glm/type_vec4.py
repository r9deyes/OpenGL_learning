# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2014 mack stone
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


class Vec4(object):

    def __init__(self, *args, **kwargs):
        if kwargs:
            self.x = kwargs.get('x', .0)
            self.y = kwargs.get('y', .0)
            self.z = kwargs.get('z', .0)
            self.w = kwargs.get('w', .0)
        elif args:
            lenArgs = len(args)
            if lenArgs == 1:
                inarg = args[0]
                if isinstance(inarg, Vec4):
                    self.x = inarg.x
                    self.y = inarg.y
                    self.z = inarg.z
                    self.w = inarg.w
                # TODO: implement vec3 and vec2
                #if isinstance(inarg, Vec3):
                elif isinstance(inarg, list) or isinstance(inarg, tuple):
                    il = []
                    if len(inarg) == 1:
                        il = inarg[0] + [.0, .0, .0]
                    elif len(inarg) == 2:
                        il = inarg[0:] + [.0, .0]
                    elif len(inarg) == 3:
                        il = inarg[0:] + [.0,]
                    elif len(inarg) == 4:
                        il = inarg
                    else:
                        il = inarg[:4]
                    self.x, self.y, self.z, self.w = il
                elif isinstance(inarg, int) or isinstance(inarg, float) or isinstance(inarg, long):
                    self.x = inarg
                    self.y = inarg
                    self.z = inarg
                    self.w = inarg
            elif lenArgs == 2:
                self.x, self.y = args
                self.z = .0
                self.w = .0
            elif lenArgs == 3:
                self.x, self.y, self.z = args
                self.w = .0
            elif lenArgs == 4:
                self.x, self.y, self.z, self.w = args
            else:
                self.x, self.y, self.z, self.w = args[:4]
        else:
            self.x = .0
            self.y = .0
            self.z = .0
            self.w = .0

    def __len__(self):
        return 4

    def __getitem__(self, index):
        if index > 3 or index < -4:
            raise IndexError('out of range')

        if index == 0 or index == -4:
            return self.x
        elif index == 1 or index == -3:
            return self.y
        elif index == 2 or index == -2:
            return self.z
        elif index == 3 or index == -1:
            return self.w
        return super(Vec4, self).__getitem__(index)

    def __setitem__(self, index, value):
        if index > 3 or index < -4:
            raise IndexError('out of range')

        if index == 0 or index == -4:
            self.x = value
        elif index == 1 or index == -3:
            self.y = value
        elif index == 2 or index == -2:
            self.z = value
        elif index == 3 or index == -1:
            self.w = value

        return super(Vec4, self).__setitem__(index, value)

