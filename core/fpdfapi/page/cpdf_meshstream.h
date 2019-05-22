// Copyright 2016 PDFium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// Original code copyright 2014 Foxit Software Inc. http://www.foxitsoftware.com

#ifndef CORE_FPDFAPI_PAGE_CPDF_MESHSTREAM_H_
#define CORE_FPDFAPI_PAGE_CPDF_MESHSTREAM_H_

#include <memory>
#include <tuple>
#include <vector>

#include "core/fpdfapi/page/cpdf_shadingpattern.h"
#include "core/fxcrt/cfx_bitstream.h"
#include "core/fxcrt/fx_system.h"
#include "core/fxcrt/retain_ptr.h"

class CPDF_StreamAcc;

class CPDF_MeshVertex {
 public:
  CPDF_MeshVertex();
  CPDF_MeshVertex(const CPDF_MeshVertex&);
  ~CPDF_MeshVertex();

  CFX_PointF position;
  float r;
  float g;
  float b;
};

class CFX_Matrix;
class CPDF_ColorSpace;
class CPDF_Function;
class CPDF_Stream;

class CPDF_MeshStream {
 public:
  CPDF_MeshStream(ShadingType type,
                  const std::vector<std::unique_ptr<CPDF_Function>>& funcs,
                  const CPDF_Stream* pShadingStream,
                  const RetainPtr<CPDF_ColorSpace>& pCS);
  ~CPDF_MeshStream();

  bool Load();

  bool CanReadFlag() const;
  bool CanReadCoords() const;
  bool CanReadColor() const;

  uint32_t ReadFlag();
  CFX_PointF ReadCoords();
  std::tuple<float, float, float> ReadColor();

  bool ReadVertex(const CFX_Matrix& pObject2Bitmap,
                  CPDF_MeshVertex* vertex,
                  uint32_t* flag);
  std::vector<CPDF_MeshVertex> ReadVertexRow(const CFX_Matrix& pObject2Bitmap,
                                             int count);

  CFX_BitStream* BitStream() { return m_BitStream.get(); }
  uint32_t ComponentBits() const { return m_nComponentBits; }
  uint32_t Components() const { return m_nComponents; }

 private:
  static const uint32_t kMaxComponents = 8;

  const ShadingType m_type;
  const std::vector<std::unique_ptr<CPDF_Function>>& m_funcs;
  UnownedPtr<const CPDF_Stream> const m_pShadingStream;
  RetainPtr<CPDF_ColorSpace> const m_pCS;
  uint32_t m_nCoordBits;
  uint32_t m_nComponentBits;
  uint32_t m_nFlagBits;
  uint32_t m_nComponents;
  uint32_t m_CoordMax;
  uint32_t m_ComponentMax;
  float m_xmin;
  float m_xmax;
  float m_ymin;
  float m_ymax;
  RetainPtr<CPDF_StreamAcc> m_pStream;
  std::unique_ptr<CFX_BitStream> m_BitStream;
  float m_ColorMin[kMaxComponents];
  float m_ColorMax[kMaxComponents];
};

#endif  // CORE_FPDFAPI_PAGE_CPDF_MESHSTREAM_H_
