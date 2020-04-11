/* GStreamer
 * Copyright (C) 2020 FIXME <fixme@example.com>
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Library General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Library General Public License for more details.
 *
 * You should have received a copy of the GNU Library General Public
 * License along with this library; if not, write to the
 * Free Software Foundation, Inc., 51 Franklin St, Fifth Floor,
 * Boston, MA 02110-1301, USA.
 */

#ifndef _GST_MLXSRC_H_
#define _GST_MLXSRC_H_

#include <gst/base/gstpushsrc.h>

G_BEGIN_DECLS

#define GST_TYPE_MLXSRC   (gst_mlxsrc_get_type())
#define GST_MLXSRC(obj)   (G_TYPE_CHECK_INSTANCE_CAST((obj),GST_TYPE_MLXSRC,GstMlxsrc))
#define GST_MLXSRC_CLASS(klass)   (G_TYPE_CHECK_CLASS_CAST((klass),GST_TYPE_MLXSRC,GstMlxsrcClass))
#define GST_IS_MLXSRC(obj)   (G_TYPE_CHECK_INSTANCE_TYPE((obj),GST_TYPE_MLXSRC))
#define GST_IS_MLXSRC_CLASS(obj)   (G_TYPE_CHECK_CLASS_TYPE((klass),GST_TYPE_MLXSRC))

typedef struct _GstMlxsrc GstMlxsrc;
typedef struct _GstMlxsrcClass GstMlxsrcClass;

struct _GstMlxsrc
{
  GstPushSrc base_mlxsrc;

};

struct _GstMlxsrcClass
{
  GstBaseSrcClass base_mlxsrc_class;
};

GType gst_mlxsrc_get_type (void);

G_END_DECLS

#endif
