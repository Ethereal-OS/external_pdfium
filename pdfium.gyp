# Copyright 2015 PDFium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

{
  'variables': {
    # TODO(thakis): Enable this, pdfium:29
    #'chromium_code': 1,

    'variables': {
      'clang_use_pdfium_plugins%': 0,
    },
    'clang_use_pdfium_plugins%': '<(clang_use_pdfium_plugins)',

    'pdf_use_skia%': 0,
    'pdf_enable_v8%': 1,
    'pdf_enable_xfa%': 0, # Set to 1 by standalone.gypi in a standalone build.
    'conditions': [
      ['OS=="linux"', {
        'bundle_freetype%': 0,
      }, {  # On Android there's no system FreeType. On Windows and Mac, only a
            # few methods are used from it.
        'bundle_freetype%': 1,
      }],
      ['clang_use_pdfium_plugins==1', {
        'variables': {
          'conditions': [
            ['OS!="win"', {
              'variables': {
                'conditions': [
                  ['OS=="mac" or OS=="ios"', {
                    'clang_lib_path%': '<!(cd <(DEPTH) && pwd -P)/third_party/llvm-build/Release+Asserts/lib/libFindBadConstructs.dylib',
                  }, { # OS != "mac" or OS != "ios"
                    'clang_lib_path%': '<!(cd <(DEPTH) && pwd -P)/third_party/llvm-build/Release+Asserts/lib/libFindBadConstructs.so',
                  }],
                ],
              },
              'clang_dynlib_flags%': '-Xclang -load -Xclang <(clang_lib_path) ',
            }, { # OS == "win"
              # On Windows, the plugin is built directly into clang, so there's
              # no need to load it dynamically.
              'clang_dynlib_flags%': '',
            }],
          ],
          'clang_plugin_args%': '-Xclang -plugin-arg-find-bad-constructs -Xclang check-templates '
          '-Xclang -plugin-arg-find-bad-constructs -Xclang follow-macro-expansion ',
        },
        'clang_pdfium_plugins_flags%':
          '<(clang_dynlib_flags)'
          '-Xclang -add-plugin -Xclang find-bad-constructs <(clang_plugin_args)',
      }],
    ],
  },
  'target_defaults': {
    'defines' : [
      'OPJ_STATIC',
      'PNG_PREFIX',
      'PNG_USE_READ_MACROS',
      'V8_DEPRECATION_WARNINGS',
      '_CRT_SECURE_NO_WARNINGS',
    ],
    'include_dirs': [
      # This is implicit in GN.
      '<(DEPTH)',
      '.',
      'third_party/freetype/include',
      'third_party/freetype/include/freetype',
    ],
    'conditions': [
      ['pdf_use_skia==1', {
        'defines': ['_SKIA_SUPPORT_'],
      }],
      ['pdf_enable_v8==1', {
        'defines': ['PDF_ENABLE_V8'],
      }],
      ['pdf_enable_xfa==1', {
        'defines': ['PDF_ENABLE_XFA'],
      }],
      ['OS=="linux"', {
        'conditions': [
          ['target_arch=="x64"', {
            'defines' : [ '_FX_CPU_=_FX_X64_', ],
            'cflags': [ '-fPIC', ],
          }],
          ['target_arch=="ia32"', {
            'defines' : [ '_FX_CPU_=_FX_X86_', ],
          }],
        ],
      }],
      ['clang==1 and clang_use_pdfium_plugins==1', {
        'cflags': [
          '<@(clang_pdfium_plugins_flags)',
        ],
      }],
    ],
    'msvs_disabled_warnings': [
      4005, 4018, 4146, 4333, 4345, 4267,
      # TODO(thestig): Fix all instances, remove this, pdfium:29
      4245, 4310, 4389, 4701, 4702, 4706,
    ],
    'variables': {
      'clang_warning_flags': [
        # TODO(thestig): Fix all instances, remove this, pdfium:29
        '-Wno-sign-compare',
      ],
      # Make sure Chromium's build/common.gypi doesn't re-add the flag on linux.
      'cflags_cc!': [ '-Wsign-compare' ],
    },
  },
  'targets': [
    {
      'target_name': 'pdfium',
      'type': 'static_library',
      'dependencies': [
        'third_party/third_party.gyp:bigint',
        'third_party/third_party.gyp:pdfium_base',
        'fdrm',
        'fpdfdoc',
        'fpdfapi',
        'fpdftext',
        'formfiller',
        'fxcodec',
        'fxcrt',
        'fxedit',
        'fxge',
        'javascript',
        'pdfwindow',
      ],
      'sources': [
        'fpdfsdk/include/fsdk_actionhandler.h',
        'fpdfsdk/include/fsdk_annothandler.h',
        'fpdfsdk/include/fsdk_baseannot.h',
        'fpdfsdk/include/fsdk_baseform.h',
        'fpdfsdk/fpdfdoc.cpp',
        'fpdfsdk/fpdfeditimg.cpp',
        'fpdfsdk/fpdfeditpage.cpp',
        'fpdfsdk/fpdfformfill.cpp',
        'fpdfsdk/fpdfppo.cpp',
        'fpdfsdk/fpdfsave.cpp',
        'fpdfsdk/fpdftext.cpp',
        'fpdfsdk/fpdfview.cpp',
        'fpdfsdk/fpdf_dataavail.cpp',
        'fpdfsdk/fpdf_ext.cpp',
        'fpdfsdk/fpdf_flatten.cpp',
        'fpdfsdk/fpdf_progressive.cpp',
        'fpdfsdk/fpdf_searchex.cpp',
        'fpdfsdk/fpdf_sysfontinfo.cpp',
        'fpdfsdk/fpdf_transformpage.cpp',
        'fpdfsdk/fsdk_actionhandler.cpp',
        'fpdfsdk/fsdk_annothandler.cpp',
        'fpdfsdk/fsdk_baseannot.cpp',
        'fpdfsdk/fsdk_baseform.cpp',
        'fpdfsdk/fsdk_mgr.cpp',
        'fpdfsdk/fsdk_rendercontext.cpp',
        'public/fpdf_dataavail.h',
        'public/fpdf_doc.h',
        'public/fpdf_edit.h',
        'public/fpdf_ext.h',
        'public/fpdf_flatten.h',
        'public/fpdf_formfill.h',
        'public/fpdf_fwlevent.h',
        'public/fpdf_ppo.h',
        'public/fpdf_progressive.h',
        'public/fpdf_save.h',
        'public/fpdf_searchex.h',
        'public/fpdf_sysfontinfo.h',
        'public/fpdf_text.h',
        'public/fpdf_transformpage.h',
        'public/fpdfview.h',
      ],
      'conditions': [
        ['pdf_enable_xfa==1', {
          'dependencies': [
            'fpdfxfa',
           ],
        }],
        ['bundle_freetype==1', {
          'dependencies': [
            'third_party/third_party.gyp:fx_freetype',
          ],
        }, {
          'link_settings': {
            'libraries': [
              '-lfreetype',
            ],
          },
        }],
      ],
      'all_dependent_settings': {
        'msvs_settings': {
          'VCLinkerTool': {
            'AdditionalDependencies': [
              'advapi32.lib',
              'gdi32.lib',
              'user32.lib',
            ],
          },
        },
        'conditions': [
          ['OS=="mac"', {
            'link_settings': {
              'libraries': [
                '$(SDKROOT)/System/Library/Frameworks/AppKit.framework',
                '$(SDKROOT)/System/Library/Frameworks/CoreFoundation.framework',
              ],
            },
          }],
        ],
      },
    },
    {
      'target_name': 'fdrm',
      'type': 'static_library',
      'sources': [
        'core/fdrm/crypto/include/fx_crypt.h',
        'core/fdrm/crypto/fx_crypt.cpp',
        'core/fdrm/crypto/fx_crypt_aes.cpp',
        'core/fdrm/crypto/fx_crypt_sha.cpp',
      ],
    },
    {
      'target_name': 'fpdfdoc',
      'type': 'static_library',
      'sources': [
        'core/include/fpdfdoc/fpdf_ap.h',
        'core/include/fpdfdoc/fpdf_doc.h',
        'core/include/fpdfdoc/fpdf_tagged.h',
        'core/include/fpdfdoc/fpdf_vt.h',
        'core/fpdfdoc/doc_action.cpp',
        'core/fpdfdoc/doc_annot.cpp',
        'core/fpdfdoc/doc_ap.cpp',
        'core/fpdfdoc/doc_basic.cpp',
        'core/fpdfdoc/doc_bookmark.cpp',
        'core/fpdfdoc/doc_form.cpp',
        'core/fpdfdoc/doc_formcontrol.cpp',
        'core/fpdfdoc/doc_formfield.cpp',
        'core/fpdfdoc/doc_link.cpp',
        'core/fpdfdoc/doc_metadata.cpp',
        'core/fpdfdoc/doc_ocg.cpp',
        'core/fpdfdoc/doc_tagged.cpp',
        'core/fpdfdoc/doc_utils.cpp',
        'core/fpdfdoc/doc_utils.h',
        'core/fpdfdoc/doc_viewerPreferences.cpp',
        'core/fpdfdoc/doc_vt.cpp',
        'core/fpdfdoc/doc_vtmodule.cpp',
        'core/fpdfdoc/pdf_vt.h',
        'core/fpdfdoc/tagged_int.h',
      ],
    },
    {
      'target_name': 'fpdfapi',
      'type': 'static_library',
      'sources': [
        'core/include/fpdfapi/cfdf_document.h',
        'core/include/fpdfapi/cpdf_array.h',
        'core/include/fpdfapi/cpdf_boolean.h',
        'core/include/fpdfapi/cpdf_dictionary.h',
        'core/include/fpdfapi/cpdf_document.h',
        'core/include/fpdfapi/cpdf_indirect_object_holder.h',
        'core/include/fpdfapi/cpdf_name.h',
        'core/include/fpdfapi/cpdf_null.h',
        'core/include/fpdfapi/cpdf_number.h',
        'core/include/fpdfapi/cpdf_object.h',
        'core/include/fpdfapi/cpdf_parser.h',
        'core/include/fpdfapi/cpdf_reference.h',
        'core/include/fpdfapi/cpdf_simple_parser.h',
        'core/include/fpdfapi/cpdf_stream.h',
        'core/include/fpdfapi/cpdf_stream_acc.h',
        'core/include/fpdfapi/cpdf_string.h',
        'core/include/fpdfapi/fpdf_module.h',
        'core/include/fpdfapi/fpdf_page.h',
        'core/include/fpdfapi/fpdf_pageobj.h',
        'core/include/fpdfapi/fpdf_parser_decode.h',
        'core/include/fpdfapi/fpdf_render.h',
        'core/include/fpdfapi/fpdf_resource.h',
        'core/include/fpdfapi/fpdf_serial.h',
        'core/include/fpdfapi/ipdf_crypto_handler.h',
        'core/include/fpdfapi/ipdf_data_avail.h',
        'core/include/fpdfapi/ipdf_security_handler.h',
        'core/fpdfapi/fpdf_basic_module.cpp',
        'core/fpdfapi/fpdf_cmaps/cmap_int.h',
        'core/fpdfapi/fpdf_cmaps/CNS1/Adobe-CNS1-UCS2_5.cpp',
        'core/fpdfapi/fpdf_cmaps/CNS1/B5pc-H_0.cpp',
        'core/fpdfapi/fpdf_cmaps/CNS1/B5pc-V_0.cpp',
        'core/fpdfapi/fpdf_cmaps/CNS1/cmaps_cns1.cpp',
        'core/fpdfapi/fpdf_cmaps/CNS1/CNS-EUC-H_0.cpp',
        'core/fpdfapi/fpdf_cmaps/CNS1/CNS-EUC-V_0.cpp',
        'core/fpdfapi/fpdf_cmaps/CNS1/ETen-B5-H_0.cpp',
        'core/fpdfapi/fpdf_cmaps/CNS1/ETen-B5-V_0.cpp',
        'core/fpdfapi/fpdf_cmaps/CNS1/ETenms-B5-H_0.cpp',
        'core/fpdfapi/fpdf_cmaps/CNS1/ETenms-B5-V_0.cpp',
        'core/fpdfapi/fpdf_cmaps/CNS1/HKscs-B5-H_5.cpp',
        'core/fpdfapi/fpdf_cmaps/CNS1/HKscs-B5-V_5.cpp',
        'core/fpdfapi/fpdf_cmaps/CNS1/UniCNS-UCS2-H_3.cpp',
        'core/fpdfapi/fpdf_cmaps/CNS1/UniCNS-UCS2-V_3.cpp',
        'core/fpdfapi/fpdf_cmaps/CNS1/UniCNS-UTF16-H_0.cpp',
        'core/fpdfapi/fpdf_cmaps/fpdf_cmaps.cpp',
        'core/fpdfapi/fpdf_cmaps/GB1/Adobe-GB1-UCS2_5.cpp',
        'core/fpdfapi/fpdf_cmaps/GB1/cmaps_gb1.cpp',
        'core/fpdfapi/fpdf_cmaps/GB1/GB-EUC-H_0.cpp',
        'core/fpdfapi/fpdf_cmaps/GB1/GB-EUC-V_0.cpp',
        'core/fpdfapi/fpdf_cmaps/GB1/GBK-EUC-H_2.cpp',
        'core/fpdfapi/fpdf_cmaps/GB1/GBK-EUC-V_2.cpp',
        'core/fpdfapi/fpdf_cmaps/GB1/GBK2K-H_5.cpp',
        'core/fpdfapi/fpdf_cmaps/GB1/GBK2K-V_5.cpp',
        'core/fpdfapi/fpdf_cmaps/GB1/GBKp-EUC-H_2.cpp',
        'core/fpdfapi/fpdf_cmaps/GB1/GBKp-EUC-V_2.cpp',
        'core/fpdfapi/fpdf_cmaps/GB1/GBpc-EUC-H_0.cpp',
        'core/fpdfapi/fpdf_cmaps/GB1/GBpc-EUC-V_0.cpp',
        'core/fpdfapi/fpdf_cmaps/GB1/UniGB-UCS2-H_4.cpp',
        'core/fpdfapi/fpdf_cmaps/GB1/UniGB-UCS2-V_4.cpp',
        'core/fpdfapi/fpdf_cmaps/Japan1/83pv-RKSJ-H_1.cpp',
        'core/fpdfapi/fpdf_cmaps/Japan1/90ms-RKSJ-H_2.cpp',
        'core/fpdfapi/fpdf_cmaps/Japan1/90ms-RKSJ-V_2.cpp',
        'core/fpdfapi/fpdf_cmaps/Japan1/90msp-RKSJ-H_2.cpp',
        'core/fpdfapi/fpdf_cmaps/Japan1/90msp-RKSJ-V_2.cpp',
        'core/fpdfapi/fpdf_cmaps/Japan1/90pv-RKSJ-H_1.cpp',
        'core/fpdfapi/fpdf_cmaps/Japan1/Add-RKSJ-H_1.cpp',
        'core/fpdfapi/fpdf_cmaps/Japan1/Add-RKSJ-V_1.cpp',
        'core/fpdfapi/fpdf_cmaps/Japan1/Adobe-Japan1-UCS2_4.cpp',
        'core/fpdfapi/fpdf_cmaps/Japan1/cmaps_japan1.cpp',
        'core/fpdfapi/fpdf_cmaps/Japan1/EUC-H_1.cpp',
        'core/fpdfapi/fpdf_cmaps/Japan1/EUC-V_1.cpp',
        'core/fpdfapi/fpdf_cmaps/Japan1/Ext-RKSJ-H_2.cpp',
        'core/fpdfapi/fpdf_cmaps/Japan1/Ext-RKSJ-V_2.cpp',
        'core/fpdfapi/fpdf_cmaps/Japan1/H_1.cpp',
        'core/fpdfapi/fpdf_cmaps/Japan1/UniJIS-UCS2-HW-H_4.cpp',
        'core/fpdfapi/fpdf_cmaps/Japan1/UniJIS-UCS2-HW-V_4.cpp',
        'core/fpdfapi/fpdf_cmaps/Japan1/UniJIS-UCS2-H_4.cpp',
        'core/fpdfapi/fpdf_cmaps/Japan1/UniJIS-UCS2-V_4.cpp',
        'core/fpdfapi/fpdf_cmaps/Japan1/V_1.cpp',
        'core/fpdfapi/fpdf_cmaps/Korea1/Adobe-Korea1-UCS2_2.cpp',
        'core/fpdfapi/fpdf_cmaps/Korea1/cmaps_korea1.cpp',
        'core/fpdfapi/fpdf_cmaps/Korea1/KSC-EUC-H_0.cpp',
        'core/fpdfapi/fpdf_cmaps/Korea1/KSC-EUC-V_0.cpp',
        'core/fpdfapi/fpdf_cmaps/Korea1/KSCms-UHC-HW-H_1.cpp',
        'core/fpdfapi/fpdf_cmaps/Korea1/KSCms-UHC-HW-V_1.cpp',
        'core/fpdfapi/fpdf_cmaps/Korea1/KSCms-UHC-H_1.cpp',
        'core/fpdfapi/fpdf_cmaps/Korea1/KSCms-UHC-V_1.cpp',
        'core/fpdfapi/fpdf_cmaps/Korea1/KSCpc-EUC-H_0.cpp',
        'core/fpdfapi/fpdf_cmaps/Korea1/UniKS-UCS2-H_1.cpp',
        'core/fpdfapi/fpdf_cmaps/Korea1/UniKS-UCS2-V_1.cpp',
        'core/fpdfapi/fpdf_cmaps/Korea1/UniKS-UTF16-H_0.cpp',
        'core/fpdfapi/fpdf_edit/editint.h',
        'core/fpdfapi/fpdf_edit/fpdf_edit_content.cpp',
        'core/fpdfapi/fpdf_edit/fpdf_edit_create.cpp',
        'core/fpdfapi/fpdf_edit/fpdf_edit_doc.cpp',
        'core/fpdfapi/fpdf_edit/fpdf_edit_image.cpp',
        'core/fpdfapi/fpdf_font/font_int.h',
        'core/fpdfapi/fpdf_font/fpdf_font.cpp',
        'core/fpdfapi/fpdf_font/fpdf_font_charset.cpp',
        'core/fpdfapi/fpdf_font/fpdf_font_cid.cpp',
        'core/fpdfapi/fpdf_font/ttgsubtable.cpp',
        'core/fpdfapi/fpdf_font/ttgsubtable.h',
        'core/fpdfapi/fpdf_page/fpdf_page.cpp',
        'core/fpdfapi/fpdf_page/fpdf_page_colors.cpp',
        'core/fpdfapi/fpdf_page/fpdf_page_doc.cpp',
        'core/fpdfapi/fpdf_page/fpdf_page_func.cpp',
        'core/fpdfapi/fpdf_page/fpdf_page_graph_state.cpp',
        'core/fpdfapi/fpdf_page/fpdf_page_image.cpp',
        'core/fpdfapi/fpdf_page/fpdf_page_parser.cpp',
        'core/fpdfapi/fpdf_page/fpdf_page_parser_old.cpp',
        'core/fpdfapi/fpdf_page/fpdf_page_path.cpp',
        'core/fpdfapi/fpdf_page/fpdf_page_pattern.cpp',
        'core/fpdfapi/fpdf_page/pageint.h',
        'core/fpdfapi/fpdf_parser/cfdf_document.cpp',
        'core/fpdfapi/fpdf_parser/cpdf_array.cpp',
        'core/fpdfapi/fpdf_parser/cpdf_boolean.cpp',
        'core/fpdfapi/fpdf_parser/cpdf_data_avail.cpp',
        'core/fpdfapi/fpdf_parser/cpdf_data_avail.h',
        'core/fpdfapi/fpdf_parser/cpdf_dictionary.cpp',
        'core/fpdfapi/fpdf_parser/cpdf_document.cpp',
        'core/fpdfapi/fpdf_parser/cpdf_hint_tables.cpp',
        'core/fpdfapi/fpdf_parser/cpdf_hint_tables.h',
        'core/fpdfapi/fpdf_parser/cpdf_indirect_object_holder.cpp',
        'core/fpdfapi/fpdf_parser/cpdf_name.cpp',
        'core/fpdfapi/fpdf_parser/cpdf_null.cpp',
        'core/fpdfapi/fpdf_parser/cpdf_number.cpp',
        'core/fpdfapi/fpdf_parser/cpdf_object.cpp',
        'core/fpdfapi/fpdf_parser/cpdf_parser.cpp',
        'core/fpdfapi/fpdf_parser/cpdf_reference.cpp',
        'core/fpdfapi/fpdf_parser/cpdf_simple_parser.cpp',
        'core/fpdfapi/fpdf_parser/cpdf_standard_crypto_handler.cpp',
        'core/fpdfapi/fpdf_parser/cpdf_standard_crypto_handler.h',
        'core/fpdfapi/fpdf_parser/cpdf_standard_security_handler.cpp',
        'core/fpdfapi/fpdf_parser/cpdf_standard_security_handler.h',
        'core/fpdfapi/fpdf_parser/cpdf_stream.cpp',
        'core/fpdfapi/fpdf_parser/cpdf_stream_acc.cpp',
        'core/fpdfapi/fpdf_parser/cpdf_string.cpp',
        'core/fpdfapi/fpdf_parser/cpdf_syntax_parser.cpp',
        'core/fpdfapi/fpdf_parser/cpdf_syntax_parser.h',
        'core/fpdfapi/fpdf_parser/fpdf_parser_decode.cpp',
        'core/fpdfapi/fpdf_parser/fpdf_parser_utility.cpp',
        'core/fpdfapi/fpdf_parser/fpdf_parser_utility.h',
        'core/fpdfapi/fpdf_render/fpdf_render.cpp',
        'core/fpdfapi/fpdf_render/fpdf_render_cache.cpp',
        'core/fpdfapi/fpdf_render/fpdf_render_image.cpp',
        'core/fpdfapi/fpdf_render/fpdf_render_loadimage.cpp',
        'core/fpdfapi/fpdf_render/fpdf_render_pattern.cpp',
        'core/fpdfapi/fpdf_render/fpdf_render_text.cpp',
        'core/fpdfapi/fpdf_render/render_int.h',
      ],
    },
    {
      'target_name': 'fpdftext',
      'type': 'static_library',
      'sources': [
        'core/fpdftext/include/ipdf_linkextract.h',
        'core/fpdftext/include/ipdf_textpage.h',
        'core/fpdftext/include/ipdf_textpagefind.h',
        'core/fpdftext/fpdf_text_int.cpp',
        'core/fpdftext/fpdf_text_int.h',
        'core/fpdftext/unicodenormalization.cpp',
        'core/fpdftext/unicodenormalization.h',
        'core/fpdftext/unicodenormalizationdata.cpp',
        'core/fpdftext/unicodenormalizationdata.h',
      ],
    },
    {
      'target_name': 'fxcodec',
      'type': 'static_library',
      'dependencies': [
        '<(libjpeg_gyp_path):libjpeg',
        'third_party/third_party.gyp:fx_lcms2',
        'third_party/third_party.gyp:fx_libopenjpeg',
        'third_party/third_party.gyp:fx_zlib',
      ],
      'sources': [
        'core/include/fxcodec/fx_codec.h',
        'core/include/fxcodec/fx_codec_def.h',
        'core/include/fxcodec/fx_codec_flate.h',
        'core/fxcodec/codec/codec_int.h',
        'core/fxcodec/codec/fx_codec.cpp',
        'core/fxcodec/codec/fx_codec_fax.cpp',
        'core/fxcodec/codec/fx_codec_flate.cpp',
        'core/fxcodec/codec/fx_codec_icc.cpp',
        'core/fxcodec/codec/fx_codec_jbig.cpp',
        'core/fxcodec/codec/fx_codec_jpeg.cpp',
        'core/fxcodec/codec/fx_codec_jpx_opj.cpp',
        'core/fxcodec/jbig2/JBig2_ArithDecoder.cpp',
        'core/fxcodec/jbig2/JBig2_ArithDecoder.h',
        'core/fxcodec/jbig2/JBig2_ArithIntDecoder.cpp',
        'core/fxcodec/jbig2/JBig2_ArithIntDecoder.h',
        'core/fxcodec/jbig2/JBig2_BitStream.cpp',
        'core/fxcodec/jbig2/JBig2_BitStream.h',
        'core/fxcodec/jbig2/JBig2_Context.cpp',
        'core/fxcodec/jbig2/JBig2_Context.h',
        'core/fxcodec/jbig2/JBig2_Define.h',
        'core/fxcodec/jbig2/JBig2_GrdProc.cpp',
        'core/fxcodec/jbig2/JBig2_GrdProc.h',
        'core/fxcodec/jbig2/JBig2_GrrdProc.cpp',
        'core/fxcodec/jbig2/JBig2_GrrdProc.h',
        'core/fxcodec/jbig2/JBig2_GsidProc.cpp',
        'core/fxcodec/jbig2/JBig2_GsidProc.h',
        'core/fxcodec/jbig2/JBig2_HtrdProc.cpp',
        'core/fxcodec/jbig2/JBig2_HtrdProc.h',
        'core/fxcodec/jbig2/JBig2_HuffmanDecoder.cpp',
        'core/fxcodec/jbig2/JBig2_HuffmanDecoder.h',
        'core/fxcodec/jbig2/JBig2_HuffmanTable.cpp',
        'core/fxcodec/jbig2/JBig2_HuffmanTable.h',
        'core/fxcodec/jbig2/JBig2_HuffmanTable_Standard.h',
        'core/fxcodec/jbig2/JBig2_Image.cpp',
        'core/fxcodec/jbig2/JBig2_Image.h',
        'core/fxcodec/jbig2/JBig2_List.h',
        'core/fxcodec/jbig2/JBig2_Page.h',
        'core/fxcodec/jbig2/JBig2_PatternDict.cpp',
        'core/fxcodec/jbig2/JBig2_PatternDict.h',
        'core/fxcodec/jbig2/JBig2_PddProc.cpp',
        'core/fxcodec/jbig2/JBig2_PddProc.h',
        'core/fxcodec/jbig2/JBig2_SddProc.cpp',
        'core/fxcodec/jbig2/JBig2_SddProc.h',
        'core/fxcodec/jbig2/JBig2_Segment.cpp',
        'core/fxcodec/jbig2/JBig2_Segment.h',
        'core/fxcodec/jbig2/JBig2_SymbolDict.cpp',
        'core/fxcodec/jbig2/JBig2_SymbolDict.h',
        'core/fxcodec/jbig2/JBig2_TrdProc.cpp',
        'core/fxcodec/jbig2/JBig2_TrdProc.h',
      ],
      'msvs_settings': {
        'VCCLCompilerTool': {
          # Unresolved warnings in fx_codec_jpx_opj.cpp
          # https://code.google.com/p/pdfium/issues/detail?id=100
          'WarnAsError': 'false',
        },
      },
      'conditions': [
        ['pdf_enable_xfa==1', {
          'dependencies': [
            'third_party/third_party.gyp:fx_lpng',
            'third_party/third_party.gyp:fx_tiff',
          ],
          'sources': [
            'core/fxcodec/codec/fx_codec_bmp.cpp',
            'core/fxcodec/codec/fx_codec_gif.cpp',
            'core/fxcodec/codec/fx_codec_png.cpp',
            'core/fxcodec/codec/fx_codec_progress.cpp',
            'core/fxcodec/codec/fx_codec_progress.h',
            'core/fxcodec/codec/fx_codec_tiff.cpp',
            'core/fxcodec/lbmp/fx_bmp.cpp',
            'core/fxcodec/lbmp/fx_bmp.h',
            'core/fxcodec/lgif/fx_gif.cpp',
            'core/fxcodec/lgif/fx_gif.h',
          ],
        }],
        ['os_posix==1', {
          # core/fxcodec/fx_libopenjpeg/src/fx_mct.c does an pointer-to-int
          # conversion to check that an address is 16-bit aligned (benign).
          'cflags_c': [ '-Wno-pointer-to-int-cast' ],
        }],
      ],
    },
    {
      'target_name': 'fxcrt',
      'type': 'static_library',
      'sources': [
        'core/include/fxcrt/fx_basic.h',
        'core/include/fxcrt/fx_bidi.h',
        'core/include/fxcrt/fx_coordinates.h',
        'core/include/fxcrt/fx_ext.h',
        'core/include/fxcrt/fx_memory.h',
        'core/include/fxcrt/fx_safe_types.h',
        'core/include/fxcrt/fx_stream.h',
        'core/include/fxcrt/fx_string.h',
        'core/include/fxcrt/fx_system.h',
        'core/include/fxcrt/fx_ucd.h',
        'core/include/fxcrt/fx_xml.h',
        'core/fxcrt/extension.h',
        'core/fxcrt/fxcrt_platforms.cpp',
        'core/fxcrt/fxcrt_platforms.h',
        'core/fxcrt/fxcrt_posix.cpp',
        'core/fxcrt/fxcrt_posix.h',
        'core/fxcrt/fxcrt_stream.cpp',
        'core/fxcrt/fxcrt_windows.cpp',
        'core/fxcrt/fxcrt_windows.h',
        'core/fxcrt/fx_basic_array.cpp',
        'core/fxcrt/fx_basic_bstring.cpp',
        'core/fxcrt/fx_basic_buffer.cpp',
        'core/fxcrt/fx_basic_coords.cpp',
        'core/fxcrt/fx_basic_gcc.cpp',
        'core/fxcrt/fx_basic_list.cpp',
        'core/fxcrt/fx_basic_memmgr.cpp',
        'core/fxcrt/fx_basic_plex.cpp',
        'core/fxcrt/fx_basic_utf.cpp',
        'core/fxcrt/fx_basic_util.cpp',
        'core/fxcrt/fx_basic_wstring.cpp',
        'core/fxcrt/fx_bidi.cpp',
        'core/fxcrt/fx_extension.cpp',
        'core/fxcrt/fx_ucddata.cpp',
        'core/fxcrt/fx_unicode.cpp',
        'core/fxcrt/fx_xml_composer.cpp',
        'core/fxcrt/fx_xml_parser.cpp',
        'core/fxcrt/plex.h',
        'core/fxcrt/xml_int.h',
      ],
      'conditions': [
        ['pdf_enable_xfa==1', {
          'sources': [
            'core/include/fxcrt/fx_arb.h',
            'core/fxcrt/fx_arabic.cpp',
            'core/fxcrt/fx_arabic.h',
            'core/fxcrt/fx_basic_maps.cpp',
          ],
        }],
      ],
    },
    {
      'target_name': 'fxge',
      'type': 'static_library',
      'dependencies': [
        'third_party/third_party.gyp:fx_agg',
      ],
      'sources': [
        'core/include/fxge/fpf.h',
        'core/include/fxge/fx_dib.h',
        'core/include/fxge/fx_font.h',
        'core/include/fxge/fx_freetype.h',
        'core/include/fxge/fx_ge.h',
        'core/include/fxge/fx_ge_apple.h',
        'core/include/fxge/fx_ge_win32.h',
        'core/fxge/agg/fx_agg_driver.h',
        'core/fxge/agg/fx_agg_driver.cpp',
        'core/fxge/android/fpf_skiafont.cpp',
        'core/fxge/android/fpf_skiafont.h',
        'core/fxge/android/fpf_skiafontmgr.cpp',
        'core/fxge/android/fpf_skiafontmgr.h',
        'core/fxge/android/fpf_skiamodule.cpp',
        'core/fxge/android/fpf_skiamodule.h',
        'core/fxge/android/fx_android_font.cpp',
        'core/fxge/android/fx_android_font.h',
        'core/fxge/android/fx_android_imp.cpp',
        'core/fxge/apple/apple_int.h',
        'core/fxge/apple/fx_apple_platform.cpp',
        'core/fxge/apple/fx_mac_imp.cpp',
        'core/fxge/apple/fx_quartz_device.cpp',
        'core/fxge/dib/dib_int.h',
        'core/fxge/dib/fx_dib_composite.cpp',
        'core/fxge/dib/fx_dib_convert.cpp',
        'core/fxge/dib/fx_dib_engine.cpp',
        'core/fxge/dib/fx_dib_main.cpp',
        'core/fxge/dib/fx_dib_transform.cpp',
        'core/fxge/fontdata/chromefontdata/chromefontdata.h',
        'core/fxge/fontdata/chromefontdata/FoxitDingbats.cpp',
        'core/fxge/fontdata/chromefontdata/FoxitFixed.cpp',
        'core/fxge/fontdata/chromefontdata/FoxitFixedBold.cpp',
        'core/fxge/fontdata/chromefontdata/FoxitFixedBoldItalic.cpp',
        'core/fxge/fontdata/chromefontdata/FoxitFixedItalic.cpp',
        'core/fxge/fontdata/chromefontdata/FoxitSans.cpp',
        'core/fxge/fontdata/chromefontdata/FoxitSansBold.cpp',
        'core/fxge/fontdata/chromefontdata/FoxitSansBoldItalic.cpp',
        'core/fxge/fontdata/chromefontdata/FoxitSansItalic.cpp',
        'core/fxge/fontdata/chromefontdata/FoxitSansMM.cpp',
        'core/fxge/fontdata/chromefontdata/FoxitSerif.cpp',
        'core/fxge/fontdata/chromefontdata/FoxitSerifBold.cpp',
        'core/fxge/fontdata/chromefontdata/FoxitSerifBoldItalic.cpp',
        'core/fxge/fontdata/chromefontdata/FoxitSerifItalic.cpp',
        'core/fxge/fontdata/chromefontdata/FoxitSerifMM.cpp',
        'core/fxge/fontdata/chromefontdata/FoxitSymbol.cpp',
        'core/fxge/freetype/fx_freetype.cpp',
        'core/fxge/ge/fx_ge.cpp',
        'core/fxge/ge/fx_ge_device.cpp',
        'core/fxge/ge/fx_ge_font.cpp',
        'core/fxge/ge/fx_ge_fontmap.cpp',
        'core/fxge/ge/fx_ge_linux.cpp',
        'core/fxge/ge/fx_ge_path.cpp',
        'core/fxge/ge/fx_ge_ps.cpp',
        'core/fxge/ge/fx_ge_text.cpp',
        'core/fxge/ge/fx_text_int.h',
      ],
      'variables': {
        'clang_warning_flags': [
          # http://code.google.com/p/pdfium/issues/detail?id=188
          '-Wno-switch',
        ],
      },
      'conditions': [
        ['pdf_use_skia==1', {
          'sources': [
            'core/fxge/skia/fx_skia_device.cpp',
          ],
          'dependencies': [
            '<(DEPTH)/skia/skia.gyp:skia',
          ],
        }],
        ['OS=="win"', {
          'defines!': [
            'WIN32_LEAN_AND_MEAN'
          ],
          'sources': [
            'core/fxge/win32/dwrite_int.h',
            'core/fxge/win32/fx_win32_device.cpp',
            'core/fxge/win32/fx_win32_dib.cpp',
            'core/fxge/win32/fx_win32_dwrite.cpp',
            'core/fxge/win32/fx_win32_gdipext.cpp',
            'core/fxge/win32/fx_win32_print.cpp',
            'core/fxge/win32/win32_int.h',
          ],
        }],
      ],
    },
    {
      'target_name': 'fxedit',
      'type': 'static_library',
      'sources': [
        'fpdfsdk/include/fxedit/fx_edit.h',
        'fpdfsdk/include/fxedit/fxet_edit.h',
        'fpdfsdk/include/fxedit/fxet_list.h',
        'fpdfsdk/fxedit/fxet_ap.cpp',
        'fpdfsdk/fxedit/fxet_edit.cpp',
        'fpdfsdk/fxedit/fxet_list.cpp',
        'fpdfsdk/fxedit/fxet_module.cpp',
        'fpdfsdk/fxedit/fxet_pageobjs.cpp',
      ],
    },
    {
      'target_name': 'pdfwindow',
      'type': 'static_library',
      'sources': [
        'fpdfsdk/include/pdfwindow/PWL_Button.h',
        'fpdfsdk/include/pdfwindow/PWL_Caret.h',
        'fpdfsdk/include/pdfwindow/PWL_ComboBox.h',
        'fpdfsdk/include/pdfwindow/PWL_Edit.h',
        'fpdfsdk/include/pdfwindow/PWL_EditCtrl.h',
        'fpdfsdk/include/pdfwindow/PWL_FontMap.h',
        'fpdfsdk/include/pdfwindow/PWL_Icon.h',
        'fpdfsdk/include/pdfwindow/PWL_IconList.h',
        'fpdfsdk/include/pdfwindow/PWL_Label.h',
        'fpdfsdk/include/pdfwindow/PWL_ListBox.h',
        'fpdfsdk/include/pdfwindow/PWL_ListCtrl.h',
        'fpdfsdk/include/pdfwindow/PWL_Note.h',
        'fpdfsdk/include/pdfwindow/PWL_ScrollBar.h',
        'fpdfsdk/include/pdfwindow/PWL_Signature.h',
        'fpdfsdk/include/pdfwindow/PWL_SpecialButton.h',
        'fpdfsdk/include/pdfwindow/PWL_Utils.h',
        'fpdfsdk/include/pdfwindow/PWL_Wnd.h',
        'fpdfsdk/pdfwindow/PWL_Button.cpp',
        'fpdfsdk/pdfwindow/PWL_Caret.cpp',
        'fpdfsdk/pdfwindow/PWL_ComboBox.cpp',
        'fpdfsdk/pdfwindow/PWL_Edit.cpp',
        'fpdfsdk/pdfwindow/PWL_EditCtrl.cpp',
        'fpdfsdk/pdfwindow/PWL_FontMap.cpp',
        'fpdfsdk/pdfwindow/PWL_Icon.cpp',
        'fpdfsdk/pdfwindow/PWL_IconList.cpp',
        'fpdfsdk/pdfwindow/PWL_Label.cpp',
        'fpdfsdk/pdfwindow/PWL_ListBox.cpp',
        'fpdfsdk/pdfwindow/PWL_ListCtrl.cpp',
        'fpdfsdk/pdfwindow/PWL_Note.cpp',
        'fpdfsdk/pdfwindow/PWL_ScrollBar.cpp',
        'fpdfsdk/pdfwindow/PWL_Signature.cpp',
        'fpdfsdk/pdfwindow/PWL_SpecialButton.cpp',
        'fpdfsdk/pdfwindow/PWL_Utils.cpp',
        'fpdfsdk/pdfwindow/PWL_Wnd.cpp',
      ],
    },
    {
      'target_name': 'javascript',
      'type': 'static_library',
      'sources': [
        'fpdfsdk/include/javascript/IJavaScript.h',
        'fpdfsdk/javascript/JS_Runtime_Stub.cpp',
      ],
      'conditions': [
        ['pdf_enable_v8==1', {
          'include_dirs': [
            '<(DEPTH)/v8',
            '<(DEPTH)/v8/include',
          ],
          'dependencies': [
            '<(DEPTH)/v8/tools/gyp/v8.gyp:v8',
          ],
          'export_dependent_settings': [
            '<(DEPTH)/v8/tools/gyp/v8.gyp:v8',
          ],
          'sources!': [
            'fpdfsdk/javascript/JS_Runtime_Stub.cpp',
          ],
          'sources': [
            'fpdfsdk/javascript/Consts.cpp',
            'fpdfsdk/javascript/Consts.h',
            'fpdfsdk/javascript/Document.cpp',
            'fpdfsdk/javascript/Document.h',
            'fpdfsdk/javascript/Field.cpp',
            'fpdfsdk/javascript/Field.h',
            'fpdfsdk/javascript/Icon.cpp',
            'fpdfsdk/javascript/Icon.h',
            'fpdfsdk/javascript/JS_Context.cpp',
            'fpdfsdk/javascript/JS_Context.h',
            'fpdfsdk/javascript/JS_Define.h',
            'fpdfsdk/javascript/JS_EventHandler.cpp',
            'fpdfsdk/javascript/JS_EventHandler.h',
            'fpdfsdk/javascript/JS_GlobalData.cpp',
            'fpdfsdk/javascript/JS_GlobalData.h',
            'fpdfsdk/javascript/JS_Object.cpp',
            'fpdfsdk/javascript/JS_Object.h',
            'fpdfsdk/javascript/JS_Runtime.cpp',
            'fpdfsdk/javascript/JS_Runtime.h',
            'fpdfsdk/javascript/JS_Value.cpp',
            'fpdfsdk/javascript/JS_Value.h',
            'fpdfsdk/javascript/PublicMethods.cpp',
            'fpdfsdk/javascript/PublicMethods.h',
            'fpdfsdk/javascript/app.cpp',
            'fpdfsdk/javascript/app.cpp',
            'fpdfsdk/javascript/app.h',
            'fpdfsdk/javascript/color.cpp',
            'fpdfsdk/javascript/color.cpp',
            'fpdfsdk/javascript/color.h',
            'fpdfsdk/javascript/console.cpp',
            'fpdfsdk/javascript/console.cpp',
            'fpdfsdk/javascript/console.h',
            'fpdfsdk/javascript/event.cpp',
            'fpdfsdk/javascript/event.h',
            'fpdfsdk/javascript/global.cpp',
            'fpdfsdk/javascript/global.h',
            'fpdfsdk/javascript/report.cpp',
            'fpdfsdk/javascript/report.h',
            'fpdfsdk/javascript/resource.cpp',
            'fpdfsdk/javascript/resource.h',
            'fpdfsdk/javascript/util.cpp',
            'fpdfsdk/javascript/util.h',
            'fpdfsdk/include/jsapi/fxjs_v8.h',
            'fpdfsdk/jsapi/fxjs_v8.cpp',
          ],
        }],
      ],
    },
    {
      'target_name': 'formfiller',
      'type': 'static_library',
      'sources': [
        'fpdfsdk/include/formfiller/FFL_CBA_Fontmap.h',
        'fpdfsdk/include/formfiller/FFL_CheckBox.h',
        'fpdfsdk/include/formfiller/FFL_ComboBox.h',
        'fpdfsdk/include/formfiller/FFL_FormFiller.h',
        'fpdfsdk/include/formfiller/FFL_IFormFiller.h',
        'fpdfsdk/include/formfiller/FFL_ListBox.h',
        'fpdfsdk/include/formfiller/FFL_PushButton.h',
        'fpdfsdk/include/formfiller/FFL_RadioButton.h',
        'fpdfsdk/include/formfiller/FFL_TextField.h',
        'fpdfsdk/formfiller/FFL_CBA_Fontmap.cpp',
        'fpdfsdk/formfiller/FFL_CheckBox.cpp',
        'fpdfsdk/formfiller/FFL_ComboBox.cpp',
        'fpdfsdk/formfiller/FFL_FormFiller.cpp',
        'fpdfsdk/formfiller/FFL_IFormFiller.cpp',
        'fpdfsdk/formfiller/FFL_ListBox.cpp',
        'fpdfsdk/formfiller/FFL_PushButton.cpp',
        'fpdfsdk/formfiller/FFL_RadioButton.cpp',
        'fpdfsdk/formfiller/FFL_TextField.cpp',
      ],
    },
    {
      'target_name': 'pdfium_unittests',
      'type': 'executable',
      'dependencies': [
        '<(DEPTH)/testing/gtest.gyp:gtest_main',
        '<(DEPTH)/testing/gtest.gyp:gtest',
        'pdfium',
        'test_support',
      ],
      'sources': [
        'core/fpdfapi/fpdf_font/fpdf_font_cid_unittest.cpp',
        'core/fpdfapi/fpdf_font/fpdf_font_unittest.cpp',
        'core/fpdfapi/fpdf_page/fpdf_page_parser_old_unittest.cpp',
        'core/fpdfapi/fpdf_parser/cpdf_object_unittest.cpp',
        'core/fpdfapi/fpdf_parser/cpdf_parser_unittest.cpp',
        'core/fpdfapi/fpdf_parser/cpdf_simple_parser_unittest.cpp',
        'core/fpdfapi/fpdf_parser/cpdf_syntax_parser_unittest.cpp',
        'core/fpdfapi/fpdf_parser/fpdf_parser_decode_unittest.cpp',
        'core/fpdfdoc/doc_basic_unittest.cpp',
        'core/fpdftext/fpdf_text_int_unittest.cpp',
        'core/fxcodec/codec/fx_codec_jpx_unittest.cpp',
        'core/fxcrt/fx_basic_bstring_unittest.cpp',
        'core/fxcrt/fx_basic_gcc_unittest.cpp',
        'core/fxcrt/fx_basic_memmgr_unittest.cpp',
        'core/fxcrt/fx_basic_wstring_unittest.cpp',
        'core/fxcrt/fx_bidi_unittest.cpp',
        'core/fxcrt/fx_extension_unittest.cpp',
        'core/fxcrt/fx_system_unittest.cpp',
        'fpdfsdk/fpdfdoc_unittest.cpp',
        'testing/fx_string_testhelpers.h',
        'testing/fx_string_testhelpers.cpp',
      ],
      'conditions': [
        ['pdf_enable_xfa==1', {
          'sources': [
            'xfa/fxbarcode/pdf417/BC_PDF417HighLevelEncoder_unittest.cpp',
            'xfa/fxfa/parser/xfa_utils_imp_unittest.cpp',
          ],
        }],
      ],
    },
    {
      'target_name': 'pdfium_embeddertests',
      'type': 'executable',
      'dependencies': [
        '<(DEPTH)/testing/gmock.gyp:gmock',
        '<(DEPTH)/testing/gtest.gyp:gtest',
        'pdfium',
        'test_support',
      ],
      'sources': [
        'core/fpdfapi/fpdf_page/fpdf_page_func_embeddertest.cpp',
        'core/fpdfapi/fpdf_parser/cpdf_parser_embeddertest.cpp',
        'core/fpdfapi/fpdf_parser/fpdf_parser_decode_embeddertest.cpp',
        'core/fpdfapi/fpdf_render/fpdf_render_loadimage_embeddertest.cpp',
        'core/fpdfapi/fpdf_render/fpdf_render_pattern_embeddertest.cpp',
        'fpdfsdk/fpdf_dataavail_embeddertest.cpp',
        'fpdfsdk/fpdfdoc_embeddertest.cpp',
        'fpdfsdk/fpdfedit_embeddertest.cpp',
        'fpdfsdk/fpdfext_embeddertest.cpp',
        'fpdfsdk/fpdfformfill_embeddertest.cpp',
        'fpdfsdk/fpdfsave_embeddertest.cpp',
        'fpdfsdk/fpdftext_embeddertest.cpp',
        'fpdfsdk/fpdfview_c_api_test.c',
        'fpdfsdk/fpdfview_c_api_test.h',
        'fpdfsdk/fpdfview_embeddertest.cpp',
        'fpdfsdk/fsdk_baseform_embeddertest.cpp',
        'testing/embedder_test.cpp',
        'testing/embedder_test.h',
        'testing/embedder_test_mock_delegate.h',
        'testing/embedder_test_timer_handling_delegate.h',
      ],
      'conditions': [
        ['pdf_enable_xfa==1', {
          'sources': [
            'xfa/fxfa/parser/xfa_parser_imp_embeddertest.cpp',
          ],
        }],
        ['pdf_enable_v8==1', {
          'include_dirs': [
            '<(DEPTH)/v8',
            '<(DEPTH)/v8/include',
          ],
          'dependencies': [
            '<(DEPTH)/v8/tools/gyp/v8.gyp:v8',
            '<(DEPTH)/v8/tools/gyp/v8.gyp:v8_libplatform',
          ],
          'sources': [
            'fpdfsdk/javascript/public_methods_embeddertest.cpp',
            'fpdfsdk/jsapi/fxjs_v8_embeddertest.cpp',
            'testing/js_embedder_test.cpp',
            'testing/js_embedder_test.h',
          ],
        }],
      ],
    },
    {
      'target_name': 'test_support',
      'type': 'static_library',
      'dependencies': [
        '<(DEPTH)/testing/gmock.gyp:gmock',
        '<(DEPTH)/testing/gtest.gyp:gtest',
      ],
      'sources': [
        'testing/fx_string_testhelpers.cpp',
        'testing/fx_string_testhelpers.h',
        'testing/test_support.cpp',
        'testing/test_support.h',
        'testing/utils/path_service.cpp',
      ],
      'conditions': [
        ['pdf_enable_v8==1', {
          'include_dirs': [
            '<(DEPTH)/v8',
            '<(DEPTH)/v8/include',
          ],
          'dependencies': [
            '<(DEPTH)/v8/tools/gyp/v8.gyp:v8',
            '<(DEPTH)/v8/tools/gyp/v8.gyp:v8_libplatform',
          ],
        }],
      ],
    },
  ],
  'conditions': [
    ['pdf_enable_xfa==1', {
      'targets': [
        {
          'target_name': 'fpdfxfa',
          'type': 'static_library',
          'dependencies': [
            'javascript',
            'xfa.gyp:xfa',
          ],
          'sources': [
            'fpdfsdk/fpdfxfa/fpdfxfa_app.cpp',
            'fpdfsdk/fpdfxfa/fpdfxfa_doc.cpp',
            'fpdfsdk/fpdfxfa/fpdfxfa_page.cpp',
            'fpdfsdk/fpdfxfa/fpdfxfa_util.cpp',
            'fpdfsdk/include/fpdfxfa/fpdfxfa_app.h',
            'fpdfsdk/include/fpdfxfa/fpdfxfa_doc.h',
            'fpdfsdk/include/fpdfxfa/fpdfxfa_page.h',
            'fpdfsdk/include/fpdfxfa/fpdfxfa_util.h',
          ],
        },
      ]
    }],
  ]
}
