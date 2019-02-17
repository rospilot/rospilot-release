/*********************************************************************
 *
 * Copyright 2012 the original author or authors.
 * See the NOTICE file distributed with this work for additional
 * information regarding copyright ownership.
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *    http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 *********************************************************************/
#ifndef ROSPILOT_TRANSCODER_H
#define ROSPILOT_TRANSCODER_H

#include<sensor_msgs/CompressedImage.h>
#include "h264_settings.h"

extern "C" {
#include <libavcodec/avcodec.h>
#include <third_party/mfc/io_dev.h>
#include <turbojpeg.h>
}

namespace rospilot {

class H264Encoder
{
public:
    virtual bool encodeInPlace(sensor_msgs::CompressedImage *image, 
            bool *keyFrame) = 0;
    
    virtual std::vector<uint8_t> getSPS() = 0;
    virtual std::vector<uint8_t> getPPS() = 0;

    virtual ~H264Encoder() {};
};

/**
 * Designed to work with the MFC hardware module in the Odroid U3.
 */
class ExynosMultiFormatCodecH264Encoder : public H264Encoder
{
private:
    std::vector<uint8_t> pps;
    std::vector<uint8_t> sps;
    io_dev *mfc;
    // Bridge to MFC input
    io_dev *inputBridge;
    // Bridge to get output from MFC
    io_dev *outputBridge;
    io_dev *deviceChain[3];
    unsigned int numPixels;

public:
    bool encodeInPlace(sensor_msgs::CompressedImage *image, bool *keyFrame) override;
    std::vector<uint8_t> getSPS();
    std::vector<uint8_t> getPPS();
    
    ExynosMultiFormatCodecH264Encoder(std::string path, H264Settings settings);

    ~ExynosMultiFormatCodecH264Encoder() override;
};

class SoftwareH264Encoder : public H264Encoder
{
private:
    int width;
    int height;
    int frameCounter = 0;
    AVCodec *encoder;
    AVPixelFormat pixelFormat;
    AVFrame *sourceFrame;
    AVCodecContext *context;

public:
    bool encodeInPlace(sensor_msgs::CompressedImage *image, bool *keyFrame) override;
    std::vector<uint8_t> getSPS();
    std::vector<uint8_t> getPPS();
    
    SoftwareH264Encoder(H264Settings settings);

private:
    AVFrame *allocFrame();
};

class JpegDecoder
{
public:
    virtual bool decodeInPlace(sensor_msgs::CompressedImage *image) = 0;

    virtual ~JpegDecoder() {};
};

class FFmpegJpegDecoder : public JpegDecoder
{
private:
    int width;
    int height;
    AVCodec *decoder;
    AVCodecContext *context;
    AVFrame *sourceFrame;
    AVFrame *outputFrame;
    AVPixelFormat outputPixelFormat;
    uint8_t *outputBuffer = new uint8_t[1];
    int outputBufferSize = 1;

public:
    bool decodeInPlace(sensor_msgs::CompressedImage *image) override;

    FFmpegJpegDecoder(int width, int height, AVPixelFormat outputPixelFormat);

    ~FFmpegJpegDecoder() override;
};

class TurboJpegDecoder : public JpegDecoder
{
private:
    tjhandle handle;
    int width;
    int height;
    uint8_t *outputBuffer = new uint8_t[1];
    int outputBufferSize = 1;

public:
    bool decodeInPlace(sensor_msgs::CompressedImage *image) override;

    TurboJpegDecoder(int width, int height, AVPixelFormat outputPixelFormat);

    ~TurboJpegDecoder() override;
};

}

#endif
