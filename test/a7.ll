; ModuleID = 'a7.c'
source_filename = "a7.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.str.1 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1

; Function Attrs: nounwind uwtable
define dso_local i32 @calculate_checksum(i32* noundef %0, i32 noundef %1) #0 !dbg !12 {
  %3 = alloca i32*, align 8
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  store i32* %0, i32** %3, align 8, !tbaa !21
  call void @llvm.dbg.declare(metadata i32** %3, metadata !16, metadata !DIExpression()), !dbg !25
  store i32 %1, i32* %4, align 4, !tbaa !26
  call void @llvm.dbg.declare(metadata i32* %4, metadata !17, metadata !DIExpression()), !dbg !28
  %7 = bitcast i32* %5 to i8*, !dbg !29
  call void @llvm.lifetime.start.p0i8(i64 4, i8* %7) #5, !dbg !29
  call void @llvm.dbg.declare(metadata i32* %5, metadata !18, metadata !DIExpression()), !dbg !30
  store i32 0, i32* %5, align 4, !dbg !30, !tbaa !26
  %8 = bitcast i32* %6 to i8*, !dbg !31
  call void @llvm.lifetime.start.p0i8(i64 4, i8* %8) #5, !dbg !31
  call void @llvm.dbg.declare(metadata i32* %6, metadata !19, metadata !DIExpression()), !dbg !32
  store i32 0, i32* %6, align 4, !dbg !32, !tbaa !26
  br label %9, !dbg !31

9:                                                ; preds = %26, %2
  %10 = load i32, i32* %6, align 4, !dbg !33, !tbaa !26
  %11 = load i32, i32* %4, align 4, !dbg !35, !tbaa !26
  %12 = icmp slt i32 %10, %11, !dbg !36
  br i1 %12, label %15, label %13, !dbg !37

13:                                               ; preds = %9
  %14 = bitcast i32* %6 to i8*, !dbg !38
  call void @llvm.lifetime.end.p0i8(i64 4, i8* %14) #5, !dbg !38
  br label %29

15:                                               ; preds = %9
  %16 = load i32, i32* %5, align 4, !dbg !39, !tbaa !26
  %17 = shl i32 %16, 5, !dbg !41
  %18 = load i32, i32* %5, align 4, !dbg !42, !tbaa !26
  %19 = add nsw i32 %17, %18, !dbg !43
  %20 = load i32*, i32** %3, align 8, !dbg !44, !tbaa !21
  %21 = load i32, i32* %6, align 4, !dbg !45, !tbaa !26
  %22 = sext i32 %21 to i64, !dbg !44
  %23 = getelementptr inbounds i32, i32* %20, i64 %22, !dbg !44
  %24 = load i32, i32* %23, align 4, !dbg !44, !tbaa !26
  %25 = add nsw i32 %19, %24, !dbg !46
  store i32 %25, i32* %5, align 4, !dbg !47, !tbaa !26
  br label %26, !dbg !48

26:                                               ; preds = %15
  %27 = load i32, i32* %6, align 4, !dbg !49, !tbaa !26
  %28 = add nsw i32 %27, 1, !dbg !49
  store i32 %28, i32* %6, align 4, !dbg !49, !tbaa !26
  br label %9, !dbg !38, !llvm.loop !50

29:                                               ; preds = %13
  %30 = load i32, i32* %5, align 4, !dbg !53, !tbaa !26
  %31 = bitcast i32* %5 to i8*, !dbg !54
  call void @llvm.lifetime.end.p0i8(i64 4, i8* %31) #5, !dbg !54
  ret i32 %30, !dbg !55
}

; Function Attrs: nofree nosync nounwind readnone speculatable willreturn
declare void @llvm.dbg.declare(metadata, metadata, metadata) #1

; Function Attrs: argmemonly nofree nosync nounwind willreturn
declare void @llvm.lifetime.start.p0i8(i64 immarg, i8* nocapture) #2

; Function Attrs: argmemonly nofree nosync nounwind willreturn
declare void @llvm.lifetime.end.p0i8(i64 immarg, i8* nocapture) #2

; Function Attrs: nounwind uwtable
define dso_local void @transform_array(i32* noundef %0, i32 noundef %1, i32 noundef %2) #0 !dbg !56 {
  %4 = alloca i32*, align 8
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  %7 = alloca i32, align 4
  store i32* %0, i32** %4, align 8, !tbaa !21
  call void @llvm.dbg.declare(metadata i32** %4, metadata !60, metadata !DIExpression()), !dbg !65
  store i32 %1, i32* %5, align 4, !tbaa !26
  call void @llvm.dbg.declare(metadata i32* %5, metadata !61, metadata !DIExpression()), !dbg !66
  store i32 %2, i32* %6, align 4, !tbaa !26
  call void @llvm.dbg.declare(metadata i32* %6, metadata !62, metadata !DIExpression()), !dbg !67
  %8 = bitcast i32* %7 to i8*, !dbg !68
  call void @llvm.lifetime.start.p0i8(i64 4, i8* %8) #5, !dbg !68
  call void @llvm.dbg.declare(metadata i32* %7, metadata !63, metadata !DIExpression()), !dbg !69
  store i32 0, i32* %7, align 4, !dbg !69, !tbaa !26
  br label %9, !dbg !68

9:                                                ; preds = %57, %3
  %10 = load i32, i32* %7, align 4, !dbg !70, !tbaa !26
  %11 = load i32, i32* %5, align 4, !dbg !72, !tbaa !26
  %12 = icmp slt i32 %10, %11, !dbg !73
  br i1 %12, label %15, label %13, !dbg !74

13:                                               ; preds = %9
  %14 = bitcast i32* %7 to i8*, !dbg !75
  call void @llvm.lifetime.end.p0i8(i64 4, i8* %14) #5, !dbg !75
  br label %60

15:                                               ; preds = %9
  %16 = load i32*, i32** %4, align 8, !dbg !76, !tbaa !21
  %17 = load i32, i32* %7, align 4, !dbg !78, !tbaa !26
  %18 = sext i32 %17 to i64, !dbg !76
  %19 = getelementptr inbounds i32, i32* %16, i64 %18, !dbg !76
  %20 = load i32, i32* %19, align 4, !dbg !76, !tbaa !26
  %21 = load i32, i32* %6, align 4, !dbg !79, !tbaa !26
  %22 = xor i32 %20, %21, !dbg !80
  %23 = load i32*, i32** %4, align 8, !dbg !81, !tbaa !21
  %24 = load i32, i32* %7, align 4, !dbg !82, !tbaa !26
  %25 = sext i32 %24 to i64, !dbg !81
  %26 = getelementptr inbounds i32, i32* %23, i64 %25, !dbg !81
  %27 = load i32, i32* %26, align 4, !dbg !81, !tbaa !26
  %28 = shl i32 %27, 4, !dbg !83
  %29 = load i32*, i32** %4, align 8, !dbg !84, !tbaa !21
  %30 = load i32, i32* %7, align 4, !dbg !85, !tbaa !26
  %31 = sext i32 %30 to i64, !dbg !84
  %32 = getelementptr inbounds i32, i32* %29, i64 %31, !dbg !84
  %33 = load i32, i32* %32, align 4, !dbg !84, !tbaa !26
  %34 = ashr i32 %33, 28, !dbg !86
  %35 = or i32 %28, %34, !dbg !87
  %36 = add nsw i32 %22, %35, !dbg !88
  %37 = load i32*, i32** %4, align 8, !dbg !89, !tbaa !21
  %38 = load i32, i32* %7, align 4, !dbg !90, !tbaa !26
  %39 = sext i32 %38 to i64, !dbg !89
  %40 = getelementptr inbounds i32, i32* %37, i64 %39, !dbg !89
  store i32 %36, i32* %40, align 4, !dbg !91, !tbaa !26
  %41 = load i32, i32* %7, align 4, !dbg !92, !tbaa !26
  %42 = icmp sgt i32 %41, 0, !dbg !94
  br i1 %42, label %43, label %56, !dbg !95

43:                                               ; preds = %15
  %44 = load i32*, i32** %4, align 8, !dbg !96, !tbaa !21
  %45 = load i32, i32* %7, align 4, !dbg !98, !tbaa !26
  %46 = sub nsw i32 %45, 1, !dbg !99
  %47 = sext i32 %46 to i64, !dbg !96
  %48 = getelementptr inbounds i32, i32* %44, i64 %47, !dbg !96
  %49 = load i32, i32* %48, align 4, !dbg !96, !tbaa !26
  %50 = load i32*, i32** %4, align 8, !dbg !100, !tbaa !21
  %51 = load i32, i32* %7, align 4, !dbg !101, !tbaa !26
  %52 = sext i32 %51 to i64, !dbg !100
  %53 = getelementptr inbounds i32, i32* %50, i64 %52, !dbg !100
  %54 = load i32, i32* %53, align 4, !dbg !102, !tbaa !26
  %55 = add nsw i32 %54, %49, !dbg !102
  store i32 %55, i32* %53, align 4, !dbg !102, !tbaa !26
  br label %56, !dbg !103

56:                                               ; preds = %43, %15
  br label %57, !dbg !104

57:                                               ; preds = %56
  %58 = load i32, i32* %7, align 4, !dbg !105, !tbaa !26
  %59 = add nsw i32 %58, 1, !dbg !105
  store i32 %59, i32* %7, align 4, !dbg !105, !tbaa !26
  br label %9, !dbg !75, !llvm.loop !106

60:                                               ; preds = %13
  ret void, !dbg !108
}

; Function Attrs: nounwind uwtable
define dso_local i32 @main() #0 !dbg !109 {
  %1 = alloca i32, align 4
  %2 = alloca i32*, align 8
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  %7 = alloca i32, align 4
  %8 = alloca i32, align 4
  %9 = alloca i32, align 4
  %10 = alloca i32, align 4
  %11 = alloca i32, align 4
  %12 = alloca i32, align 4
  store i32 0, i32* %1, align 4
  %13 = bitcast i32** %2 to i8*, !dbg !135
  call void @llvm.lifetime.start.p0i8(i64 8, i8* %13) #5, !dbg !135
  call void @llvm.dbg.declare(metadata i32** %2, metadata !113, metadata !DIExpression()), !dbg !136
  %14 = call noalias i8* @malloc(i64 noundef 4000) #5, !dbg !137
  %15 = bitcast i8* %14 to i32*, !dbg !138
  store i32* %15, i32** %2, align 8, !dbg !136, !tbaa !21
  %16 = bitcast i32* %3 to i8*, !dbg !139
  call void @llvm.lifetime.start.p0i8(i64 4, i8* %16) #5, !dbg !139
  call void @llvm.dbg.declare(metadata i32* %3, metadata !114, metadata !DIExpression()), !dbg !140
  store i32 0, i32* %3, align 4, !dbg !140, !tbaa !26
  %17 = bitcast i32* %4 to i8*, !dbg !141
  call void @llvm.lifetime.start.p0i8(i64 4, i8* %17) #5, !dbg !141
  call void @llvm.dbg.declare(metadata i32* %4, metadata !115, metadata !DIExpression()), !dbg !142
  store i32 0, i32* %4, align 4, !dbg !142, !tbaa !26
  br label %18, !dbg !141

18:                                               ; preds = %32, %0
  %19 = load i32, i32* %4, align 4, !dbg !143, !tbaa !26
  %20 = icmp slt i32 %19, 1000, !dbg !145
  br i1 %20, label %23, label %21, !dbg !146

21:                                               ; preds = %18
  %22 = bitcast i32* %4 to i8*, !dbg !147
  call void @llvm.lifetime.end.p0i8(i64 4, i8* %22) #5, !dbg !147
  br label %35

23:                                               ; preds = %18
  %24 = load i32, i32* %4, align 4, !dbg !148, !tbaa !26
  %25 = mul nsw i32 %24, 1103515245, !dbg !150
  %26 = add nsw i32 %25, 12345, !dbg !151
  %27 = and i32 %26, 2147483647, !dbg !152
  %28 = load i32*, i32** %2, align 8, !dbg !153, !tbaa !21
  %29 = load i32, i32* %4, align 4, !dbg !154, !tbaa !26
  %30 = sext i32 %29 to i64, !dbg !153
  %31 = getelementptr inbounds i32, i32* %28, i64 %30, !dbg !153
  store i32 %27, i32* %31, align 4, !dbg !155, !tbaa !26
  br label %32, !dbg !156

32:                                               ; preds = %23
  %33 = load i32, i32* %4, align 4, !dbg !157, !tbaa !26
  %34 = add nsw i32 %33, 1, !dbg !157
  store i32 %34, i32* %4, align 4, !dbg !157, !tbaa !26
  br label %18, !dbg !147, !llvm.loop !158

35:                                               ; preds = %21
  %36 = bitcast i32* %5 to i8*, !dbg !160
  call void @llvm.lifetime.start.p0i8(i64 4, i8* %36) #5, !dbg !160
  call void @llvm.dbg.declare(metadata i32* %5, metadata !117, metadata !DIExpression()), !dbg !161
  %37 = call i32 (i8*, ...) @__isoc99_scanf(i8* noundef getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* noundef %5), !dbg !162
  %38 = bitcast i32* %6 to i8*, !dbg !163
  call void @llvm.lifetime.start.p0i8(i64 4, i8* %38) #5, !dbg !163
  call void @llvm.dbg.declare(metadata i32* %6, metadata !118, metadata !DIExpression()), !dbg !164
  store i32 0, i32* %6, align 4, !dbg !164, !tbaa !26
  br label %39, !dbg !163

39:                                               ; preds = %122, %35
  %40 = load i32, i32* %6, align 4, !dbg !165, !tbaa !26
  %41 = load i32, i32* %5, align 4, !dbg !166, !tbaa !26
  %42 = icmp slt i32 %40, %41, !dbg !167
  br i1 %42, label %45, label %43, !dbg !168

43:                                               ; preds = %39
  store i32 5, i32* %7, align 4
  %44 = bitcast i32* %6 to i8*, !dbg !169
  call void @llvm.lifetime.end.p0i8(i64 4, i8* %44) #5, !dbg !169
  br label %125

45:                                               ; preds = %39
  %46 = bitcast i32* %8 to i8*, !dbg !170
  call void @llvm.lifetime.start.p0i8(i64 4, i8* %46) #5, !dbg !170
  call void @llvm.dbg.declare(metadata i32* %8, metadata !120, metadata !DIExpression()), !dbg !171
  store i32 0, i32* %8, align 4, !dbg !171, !tbaa !26
  br label %47, !dbg !170

47:                                               ; preds = %114, %45
  %48 = load i32, i32* %8, align 4, !dbg !172, !tbaa !26
  %49 = icmp slt i32 %48, 5, !dbg !173
  br i1 %49, label %52, label %50, !dbg !174

50:                                               ; preds = %47
  store i32 8, i32* %7, align 4
  %51 = bitcast i32* %8 to i8*, !dbg !175
  call void @llvm.lifetime.end.p0i8(i64 4, i8* %51) #5, !dbg !175
  br label %117

52:                                               ; preds = %47
  %53 = bitcast i32* %9 to i8*, !dbg !176
  call void @llvm.lifetime.start.p0i8(i64 4, i8* %53) #5, !dbg !176
  call void @llvm.dbg.declare(metadata i32* %9, metadata !124, metadata !DIExpression()), !dbg !177
  %54 = load i32, i32* %6, align 4, !dbg !178, !tbaa !26
  %55 = load i32, i32* %8, align 4, !dbg !179, !tbaa !26
  %56 = mul nsw i32 %54, %55, !dbg !180
  %57 = mul nsw i32 %56, 16807, !dbg !181
  %58 = and i32 %57, 65535, !dbg !182
  store i32 %58, i32* %9, align 4, !dbg !177, !tbaa !26
  %59 = load i32*, i32** %2, align 8, !dbg !183, !tbaa !21
  %60 = load i32, i32* %9, align 4, !dbg !184, !tbaa !26
  call void @transform_array(i32* noundef %59, i32 noundef 1000, i32 noundef %60), !dbg !185
  %61 = bitcast i32* %10 to i8*, !dbg !186
  call void @llvm.lifetime.start.p0i8(i64 4, i8* %61) #5, !dbg !186
  call void @llvm.dbg.declare(metadata i32* %10, metadata !127, metadata !DIExpression()), !dbg !187
  %62 = load i32*, i32** %2, align 8, !dbg !188, !tbaa !21
  %63 = call i32 @calculate_checksum(i32* noundef %62, i32 noundef 1000), !dbg !189
  store i32 %63, i32* %10, align 4, !dbg !187, !tbaa !26
  %64 = load i32, i32* %10, align 4, !dbg !190, !tbaa !26
  %65 = and i32 %64, 1, !dbg !191
  %66 = icmp ne i32 %65, 0, !dbg !191
  br i1 %66, label %67, label %89, !dbg !192

67:                                               ; preds = %52
  %68 = bitcast i32* %11 to i8*, !dbg !193
  call void @llvm.lifetime.start.p0i8(i64 4, i8* %68) #5, !dbg !193
  call void @llvm.dbg.declare(metadata i32* %11, metadata !128, metadata !DIExpression()), !dbg !194
  store i32 0, i32* %11, align 4, !dbg !194, !tbaa !26
  br label %69, !dbg !193

69:                                               ; preds = %85, %67
  %70 = load i32, i32* %11, align 4, !dbg !195, !tbaa !26
  %71 = icmp slt i32 %70, 1000, !dbg !197
  br i1 %71, label %74, label %72, !dbg !198

72:                                               ; preds = %69
  store i32 11, i32* %7, align 4
  %73 = bitcast i32* %11 to i8*, !dbg !199
  call void @llvm.lifetime.end.p0i8(i64 4, i8* %73) #5, !dbg !199
  br label %88

74:                                               ; preds = %69
  %75 = load i32*, i32** %2, align 8, !dbg !200, !tbaa !21
  %76 = load i32, i32* %11, align 4, !dbg !202, !tbaa !26
  %77 = sext i32 %76 to i64, !dbg !200
  %78 = getelementptr inbounds i32, i32* %75, i64 %77, !dbg !200
  %79 = load i32, i32* %78, align 4, !dbg !200, !tbaa !26
  %80 = xor i32 %79, -1, !dbg !203
  %81 = load i32*, i32** %2, align 8, !dbg !204, !tbaa !21
  %82 = load i32, i32* %11, align 4, !dbg !205, !tbaa !26
  %83 = sext i32 %82 to i64, !dbg !204
  %84 = getelementptr inbounds i32, i32* %81, i64 %83, !dbg !204
  store i32 %80, i32* %84, align 4, !dbg !206, !tbaa !26
  br label %85, !dbg !207

85:                                               ; preds = %74
  %86 = load i32, i32* %11, align 4, !dbg !208, !tbaa !26
  %87 = add nsw i32 %86, 2, !dbg !208
  store i32 %87, i32* %11, align 4, !dbg !208, !tbaa !26
  br label %69, !dbg !199, !llvm.loop !209

88:                                               ; preds = %72
  br label %111, !dbg !211

89:                                               ; preds = %52
  %90 = bitcast i32* %12 to i8*, !dbg !212
  call void @llvm.lifetime.start.p0i8(i64 4, i8* %90) #5, !dbg !212
  call void @llvm.dbg.declare(metadata i32* %12, metadata !132, metadata !DIExpression()), !dbg !213
  store i32 1, i32* %12, align 4, !dbg !213, !tbaa !26
  br label %91, !dbg !212

91:                                               ; preds = %107, %89
  %92 = load i32, i32* %12, align 4, !dbg !214, !tbaa !26
  %93 = icmp slt i32 %92, 1000, !dbg !216
  br i1 %93, label %96, label %94, !dbg !217

94:                                               ; preds = %91
  store i32 14, i32* %7, align 4
  %95 = bitcast i32* %12 to i8*, !dbg !218
  call void @llvm.lifetime.end.p0i8(i64 4, i8* %95) #5, !dbg !218
  br label %110

96:                                               ; preds = %91
  %97 = load i32*, i32** %2, align 8, !dbg !219, !tbaa !21
  %98 = load i32, i32* %12, align 4, !dbg !221, !tbaa !26
  %99 = sext i32 %98 to i64, !dbg !219
  %100 = getelementptr inbounds i32, i32* %97, i64 %99, !dbg !219
  %101 = load i32, i32* %100, align 4, !dbg !219, !tbaa !26
  %102 = ashr i32 %101, 1, !dbg !222
  %103 = load i32*, i32** %2, align 8, !dbg !223, !tbaa !21
  %104 = load i32, i32* %12, align 4, !dbg !224, !tbaa !26
  %105 = sext i32 %104 to i64, !dbg !223
  %106 = getelementptr inbounds i32, i32* %103, i64 %105, !dbg !223
  store i32 %102, i32* %106, align 4, !dbg !225, !tbaa !26
  br label %107, !dbg !226

107:                                              ; preds = %96
  %108 = load i32, i32* %12, align 4, !dbg !227, !tbaa !26
  %109 = add nsw i32 %108, 2, !dbg !227
  store i32 %109, i32* %12, align 4, !dbg !227, !tbaa !26
  br label %91, !dbg !218, !llvm.loop !228

110:                                              ; preds = %94
  br label %111

111:                                              ; preds = %110, %88
  %112 = bitcast i32* %10 to i8*, !dbg !230
  call void @llvm.lifetime.end.p0i8(i64 4, i8* %112) #5, !dbg !230
  %113 = bitcast i32* %9 to i8*, !dbg !230
  call void @llvm.lifetime.end.p0i8(i64 4, i8* %113) #5, !dbg !230
  br label %114, !dbg !231

114:                                              ; preds = %111
  %115 = load i32, i32* %8, align 4, !dbg !232, !tbaa !26
  %116 = add nsw i32 %115, 1, !dbg !232
  store i32 %116, i32* %8, align 4, !dbg !232, !tbaa !26
  br label %47, !dbg !175, !llvm.loop !233

117:                                              ; preds = %50
  %118 = load i32*, i32** %2, align 8, !dbg !235, !tbaa !21
  %119 = call i32 @calculate_checksum(i32* noundef %118, i32 noundef 1000), !dbg !236
  %120 = load i32, i32* %3, align 4, !dbg !237, !tbaa !26
  %121 = xor i32 %120, %119, !dbg !237
  store i32 %121, i32* %3, align 4, !dbg !237, !tbaa !26
  br label %122, !dbg !238

122:                                              ; preds = %117
  %123 = load i32, i32* %6, align 4, !dbg !239, !tbaa !26
  %124 = add nsw i32 %123, 1, !dbg !239
  store i32 %124, i32* %6, align 4, !dbg !239, !tbaa !26
  br label %39, !dbg !169, !llvm.loop !240

125:                                              ; preds = %43
  %126 = load i32*, i32** %2, align 8, !dbg !242, !tbaa !21
  %127 = bitcast i32* %126 to i8*, !dbg !242
  call void @free(i8* noundef %127) #5, !dbg !243
  %128 = load i32, i32* %3, align 4, !dbg !244, !tbaa !26
  %129 = call i32 (i8*, ...) @printf(i8* noundef getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 noundef %128), !dbg !245
  store i32 0, i32* %1, align 4, !dbg !246
  store i32 1, i32* %7, align 4
  %130 = bitcast i32* %5 to i8*, !dbg !247
  call void @llvm.lifetime.end.p0i8(i64 4, i8* %130) #5, !dbg !247
  %131 = bitcast i32* %3 to i8*, !dbg !247
  call void @llvm.lifetime.end.p0i8(i64 4, i8* %131) #5, !dbg !247
  %132 = bitcast i32** %2 to i8*, !dbg !247
  call void @llvm.lifetime.end.p0i8(i64 8, i8* %132) #5, !dbg !247
  %133 = load i32, i32* %1, align 4, !dbg !247
  ret i32 %133, !dbg !247
}

; Function Attrs: nounwind
declare noalias i8* @malloc(i64 noundef) #3

declare i32 @__isoc99_scanf(i8* noundef, ...) #4

; Function Attrs: nounwind
declare void @free(i8* noundef) #3

declare i32 @printf(i8* noundef, ...) #4

attributes #0 = { nounwind uwtable "frame-pointer"="none" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { nofree nosync nounwind readnone speculatable willreturn }
attributes #2 = { argmemonly nofree nosync nounwind willreturn }
attributes #3 = { nounwind "frame-pointer"="none" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #4 = { "frame-pointer"="none" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #5 = { nounwind }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!5, !6, !7, !8, !9, !10}
!llvm.ident = !{!11}

!0 = distinct !DICompileUnit(language: DW_LANG_C99, file: !1, producer: "Ubuntu clang version 14.0.0-1ubuntu1.1", isOptimized: true, runtimeVersion: 0, emissionKind: FullDebug, retainedTypes: !2, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "a7.c", directory: "/home/tsq/llvm_pipeline_engineering/test", checksumkind: CSK_MD5, checksum: "38429bde42bac525f4d44b6d06b1f2ee")
!2 = !{!3}
!3 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !4, size: 64)
!4 = !DIBasicType(name: "int", size: 32, encoding: DW_ATE_signed)
!5 = !{i32 7, !"Dwarf Version", i32 5}
!6 = !{i32 2, !"Debug Info Version", i32 3}
!7 = !{i32 1, !"wchar_size", i32 4}
!8 = !{i32 7, !"PIC Level", i32 2}
!9 = !{i32 7, !"PIE Level", i32 2}
!10 = !{i32 7, !"uwtable", i32 1}
!11 = !{!"Ubuntu clang version 14.0.0-1ubuntu1.1"}
!12 = distinct !DISubprogram(name: "calculate_checksum", scope: !1, file: !1, line: 15, type: !13, scopeLine: 15, flags: DIFlagPrototyped | DIFlagAllCallsDescribed, spFlags: DISPFlagDefinition | DISPFlagOptimized, unit: !0, retainedNodes: !15)
!13 = !DISubroutineType(types: !14)
!14 = !{!4, !3, !4}
!15 = !{!16, !17, !18, !19}
!16 = !DILocalVariable(name: "arr", arg: 1, scope: !12, file: !1, line: 15, type: !3)
!17 = !DILocalVariable(name: "size", arg: 2, scope: !12, file: !1, line: 15, type: !4)
!18 = !DILocalVariable(name: "checksum", scope: !12, file: !1, line: 16, type: !4)
!19 = !DILocalVariable(name: "i", scope: !20, file: !1, line: 17, type: !4)
!20 = distinct !DILexicalBlock(scope: !12, file: !1, line: 17, column: 5)
!21 = !{!22, !22, i64 0}
!22 = !{!"any pointer", !23, i64 0}
!23 = !{!"omnipotent char", !24, i64 0}
!24 = !{!"Simple C/C++ TBAA"}
!25 = !DILocation(line: 15, column: 29, scope: !12)
!26 = !{!27, !27, i64 0}
!27 = !{!"int", !23, i64 0}
!28 = !DILocation(line: 15, column: 38, scope: !12)
!29 = !DILocation(line: 16, column: 5, scope: !12)
!30 = !DILocation(line: 16, column: 9, scope: !12)
!31 = !DILocation(line: 17, column: 10, scope: !20)
!32 = !DILocation(line: 17, column: 14, scope: !20)
!33 = !DILocation(line: 17, column: 21, scope: !34)
!34 = distinct !DILexicalBlock(scope: !20, file: !1, line: 17, column: 5)
!35 = !DILocation(line: 17, column: 25, scope: !34)
!36 = !DILocation(line: 17, column: 23, scope: !34)
!37 = !DILocation(line: 17, column: 5, scope: !20)
!38 = !DILocation(line: 17, column: 5, scope: !34)
!39 = !DILocation(line: 18, column: 22, scope: !40)
!40 = distinct !DILexicalBlock(scope: !34, file: !1, line: 17, column: 36)
!41 = !DILocation(line: 18, column: 31, scope: !40)
!42 = !DILocation(line: 18, column: 39, scope: !40)
!43 = !DILocation(line: 18, column: 37, scope: !40)
!44 = !DILocation(line: 18, column: 51, scope: !40)
!45 = !DILocation(line: 18, column: 55, scope: !40)
!46 = !DILocation(line: 18, column: 49, scope: !40)
!47 = !DILocation(line: 18, column: 18, scope: !40)
!48 = !DILocation(line: 19, column: 5, scope: !40)
!49 = !DILocation(line: 17, column: 32, scope: !34)
!50 = distinct !{!50, !37, !51, !52}
!51 = !DILocation(line: 19, column: 5, scope: !20)
!52 = !{!"llvm.loop.mustprogress"}
!53 = !DILocation(line: 20, column: 12, scope: !12)
!54 = !DILocation(line: 21, column: 1, scope: !12)
!55 = !DILocation(line: 20, column: 5, scope: !12)
!56 = distinct !DISubprogram(name: "transform_array", scope: !1, file: !1, line: 23, type: !57, scopeLine: 23, flags: DIFlagPrototyped | DIFlagAllCallsDescribed, spFlags: DISPFlagDefinition | DISPFlagOptimized, unit: !0, retainedNodes: !59)
!57 = !DISubroutineType(types: !58)
!58 = !{null, !3, !4, !4}
!59 = !{!60, !61, !62, !63}
!60 = !DILocalVariable(name: "arr", arg: 1, scope: !56, file: !1, line: 23, type: !3)
!61 = !DILocalVariable(name: "size", arg: 2, scope: !56, file: !1, line: 23, type: !4)
!62 = !DILocalVariable(name: "key", arg: 3, scope: !56, file: !1, line: 23, type: !4)
!63 = !DILocalVariable(name: "i", scope: !64, file: !1, line: 24, type: !4)
!64 = distinct !DILexicalBlock(scope: !56, file: !1, line: 24, column: 5)
!65 = !DILocation(line: 23, column: 27, scope: !56)
!66 = !DILocation(line: 23, column: 36, scope: !56)
!67 = !DILocation(line: 23, column: 46, scope: !56)
!68 = !DILocation(line: 24, column: 10, scope: !64)
!69 = !DILocation(line: 24, column: 14, scope: !64)
!70 = !DILocation(line: 24, column: 21, scope: !71)
!71 = distinct !DILexicalBlock(scope: !64, file: !1, line: 24, column: 5)
!72 = !DILocation(line: 24, column: 25, scope: !71)
!73 = !DILocation(line: 24, column: 23, scope: !71)
!74 = !DILocation(line: 24, column: 5, scope: !64)
!75 = !DILocation(line: 24, column: 5, scope: !71)
!76 = !DILocation(line: 25, column: 19, scope: !77)
!77 = distinct !DILexicalBlock(scope: !71, file: !1, line: 24, column: 36)
!78 = !DILocation(line: 25, column: 23, scope: !77)
!79 = !DILocation(line: 25, column: 28, scope: !77)
!80 = !DILocation(line: 25, column: 26, scope: !77)
!81 = !DILocation(line: 25, column: 37, scope: !77)
!82 = !DILocation(line: 25, column: 41, scope: !77)
!83 = !DILocation(line: 25, column: 44, scope: !77)
!84 = !DILocation(line: 25, column: 53, scope: !77)
!85 = !DILocation(line: 25, column: 57, scope: !77)
!86 = !DILocation(line: 25, column: 60, scope: !77)
!87 = !DILocation(line: 25, column: 50, scope: !77)
!88 = !DILocation(line: 25, column: 33, scope: !77)
!89 = !DILocation(line: 25, column: 9, scope: !77)
!90 = !DILocation(line: 25, column: 13, scope: !77)
!91 = !DILocation(line: 25, column: 16, scope: !77)
!92 = !DILocation(line: 26, column: 13, scope: !93)
!93 = distinct !DILexicalBlock(scope: !77, file: !1, line: 26, column: 13)
!94 = !DILocation(line: 26, column: 15, scope: !93)
!95 = !DILocation(line: 26, column: 13, scope: !77)
!96 = !DILocation(line: 27, column: 23, scope: !97)
!97 = distinct !DILexicalBlock(scope: !93, file: !1, line: 26, column: 20)
!98 = !DILocation(line: 27, column: 27, scope: !97)
!99 = !DILocation(line: 27, column: 28, scope: !97)
!100 = !DILocation(line: 27, column: 13, scope: !97)
!101 = !DILocation(line: 27, column: 17, scope: !97)
!102 = !DILocation(line: 27, column: 20, scope: !97)
!103 = !DILocation(line: 28, column: 9, scope: !97)
!104 = !DILocation(line: 29, column: 5, scope: !77)
!105 = !DILocation(line: 24, column: 32, scope: !71)
!106 = distinct !{!106, !74, !107, !52}
!107 = !DILocation(line: 29, column: 5, scope: !64)
!108 = !DILocation(line: 30, column: 1, scope: !56)
!109 = distinct !DISubprogram(name: "main", scope: !1, file: !1, line: 32, type: !110, scopeLine: 32, flags: DIFlagAllCallsDescribed, spFlags: DISPFlagDefinition | DISPFlagOptimized, unit: !0, retainedNodes: !112)
!110 = !DISubroutineType(types: !111)
!111 = !{!4}
!112 = !{!113, !114, !115, !117, !118, !120, !124, !127, !128, !132}
!113 = !DILocalVariable(name: "data", scope: !109, file: !1, line: 33, type: !3)
!114 = !DILocalVariable(name: "result", scope: !109, file: !1, line: 34, type: !4)
!115 = !DILocalVariable(name: "i", scope: !116, file: !1, line: 37, type: !4)
!116 = distinct !DILexicalBlock(scope: !109, file: !1, line: 37, column: 5)
!117 = !DILocalVariable(name: "iterations", scope: !109, file: !1, line: 41, type: !4)
!118 = !DILocalVariable(name: "iter", scope: !119, file: !1, line: 44, type: !4)
!119 = distinct !DILexicalBlock(scope: !109, file: !1, line: 44, column: 5)
!120 = !DILocalVariable(name: "j", scope: !121, file: !1, line: 46, type: !4)
!121 = distinct !DILexicalBlock(scope: !122, file: !1, line: 46, column: 9)
!122 = distinct !DILexicalBlock(scope: !123, file: !1, line: 44, column: 51)
!123 = distinct !DILexicalBlock(scope: !119, file: !1, line: 44, column: 5)
!124 = !DILocalVariable(name: "key", scope: !125, file: !1, line: 47, type: !4)
!125 = distinct !DILexicalBlock(scope: !126, file: !1, line: 46, column: 37)
!126 = distinct !DILexicalBlock(scope: !121, file: !1, line: 46, column: 9)
!127 = !DILocalVariable(name: "checksum", scope: !125, file: !1, line: 51, type: !4)
!128 = !DILocalVariable(name: "k", scope: !129, file: !1, line: 53, type: !4)
!129 = distinct !DILexicalBlock(scope: !130, file: !1, line: 53, column: 17)
!130 = distinct !DILexicalBlock(scope: !131, file: !1, line: 52, column: 31)
!131 = distinct !DILexicalBlock(scope: !125, file: !1, line: 52, column: 17)
!132 = !DILocalVariable(name: "k", scope: !133, file: !1, line: 57, type: !4)
!133 = distinct !DILexicalBlock(scope: !134, file: !1, line: 57, column: 17)
!134 = distinct !DILexicalBlock(scope: !131, file: !1, line: 56, column: 20)
!135 = !DILocation(line: 33, column: 5, scope: !109)
!136 = !DILocation(line: 33, column: 10, scope: !109)
!137 = !DILocation(line: 33, column: 23, scope: !109)
!138 = !DILocation(line: 33, column: 17, scope: !109)
!139 = !DILocation(line: 34, column: 5, scope: !109)
!140 = !DILocation(line: 34, column: 9, scope: !109)
!141 = !DILocation(line: 37, column: 10, scope: !116)
!142 = !DILocation(line: 37, column: 14, scope: !116)
!143 = !DILocation(line: 37, column: 21, scope: !144)
!144 = distinct !DILexicalBlock(scope: !116, file: !1, line: 37, column: 5)
!145 = !DILocation(line: 37, column: 23, scope: !144)
!146 = !DILocation(line: 37, column: 5, scope: !116)
!147 = !DILocation(line: 37, column: 5, scope: !144)
!148 = !DILocation(line: 38, column: 20, scope: !149)
!149 = distinct !DILexicalBlock(scope: !144, file: !1, line: 37, column: 36)
!150 = !DILocation(line: 38, column: 22, scope: !149)
!151 = !DILocation(line: 38, column: 35, scope: !149)
!152 = !DILocation(line: 38, column: 44, scope: !149)
!153 = !DILocation(line: 38, column: 9, scope: !149)
!154 = !DILocation(line: 38, column: 14, scope: !149)
!155 = !DILocation(line: 38, column: 17, scope: !149)
!156 = !DILocation(line: 39, column: 5, scope: !149)
!157 = !DILocation(line: 37, column: 32, scope: !144)
!158 = distinct !{!158, !146, !159, !52}
!159 = !DILocation(line: 39, column: 5, scope: !116)
!160 = !DILocation(line: 41, column: 5, scope: !109)
!161 = !DILocation(line: 41, column: 9, scope: !109)
!162 = !DILocation(line: 42, column: 5, scope: !109)
!163 = !DILocation(line: 44, column: 10, scope: !119)
!164 = !DILocation(line: 44, column: 14, scope: !119)
!165 = !DILocation(line: 44, column: 24, scope: !123)
!166 = !DILocation(line: 44, column: 31, scope: !123)
!167 = !DILocation(line: 44, column: 29, scope: !123)
!168 = !DILocation(line: 44, column: 5, scope: !119)
!169 = !DILocation(line: 44, column: 5, scope: !123)
!170 = !DILocation(line: 46, column: 14, scope: !121)
!171 = !DILocation(line: 46, column: 18, scope: !121)
!172 = !DILocation(line: 46, column: 25, scope: !126)
!173 = !DILocation(line: 46, column: 27, scope: !126)
!174 = !DILocation(line: 46, column: 9, scope: !121)
!175 = !DILocation(line: 46, column: 9, scope: !126)
!176 = !DILocation(line: 47, column: 13, scope: !125)
!177 = !DILocation(line: 47, column: 17, scope: !125)
!178 = !DILocation(line: 47, column: 24, scope: !125)
!179 = !DILocation(line: 47, column: 31, scope: !125)
!180 = !DILocation(line: 47, column: 29, scope: !125)
!181 = !DILocation(line: 47, column: 33, scope: !125)
!182 = !DILocation(line: 47, column: 42, scope: !125)
!183 = !DILocation(line: 48, column: 29, scope: !125)
!184 = !DILocation(line: 48, column: 41, scope: !125)
!185 = !DILocation(line: 48, column: 13, scope: !125)
!186 = !DILocation(line: 51, column: 13, scope: !125)
!187 = !DILocation(line: 51, column: 17, scope: !125)
!188 = !DILocation(line: 51, column: 47, scope: !125)
!189 = !DILocation(line: 51, column: 28, scope: !125)
!190 = !DILocation(line: 52, column: 17, scope: !131)
!191 = !DILocation(line: 52, column: 26, scope: !131)
!192 = !DILocation(line: 52, column: 17, scope: !125)
!193 = !DILocation(line: 53, column: 22, scope: !129)
!194 = !DILocation(line: 53, column: 26, scope: !129)
!195 = !DILocation(line: 53, column: 33, scope: !196)
!196 = distinct !DILexicalBlock(scope: !129, file: !1, line: 53, column: 17)
!197 = !DILocation(line: 53, column: 35, scope: !196)
!198 = !DILocation(line: 53, column: 17, scope: !129)
!199 = !DILocation(line: 53, column: 17, scope: !196)
!200 = !DILocation(line: 54, column: 32, scope: !201)
!201 = distinct !DILexicalBlock(scope: !196, file: !1, line: 53, column: 51)
!202 = !DILocation(line: 54, column: 37, scope: !201)
!203 = !DILocation(line: 54, column: 31, scope: !201)
!204 = !DILocation(line: 54, column: 21, scope: !201)
!205 = !DILocation(line: 54, column: 26, scope: !201)
!206 = !DILocation(line: 54, column: 29, scope: !201)
!207 = !DILocation(line: 55, column: 17, scope: !201)
!208 = !DILocation(line: 53, column: 45, scope: !196)
!209 = distinct !{!209, !198, !210, !52}
!210 = !DILocation(line: 55, column: 17, scope: !129)
!211 = !DILocation(line: 56, column: 13, scope: !130)
!212 = !DILocation(line: 57, column: 22, scope: !133)
!213 = !DILocation(line: 57, column: 26, scope: !133)
!214 = !DILocation(line: 57, column: 33, scope: !215)
!215 = distinct !DILexicalBlock(scope: !133, file: !1, line: 57, column: 17)
!216 = !DILocation(line: 57, column: 35, scope: !215)
!217 = !DILocation(line: 57, column: 17, scope: !133)
!218 = !DILocation(line: 57, column: 17, scope: !215)
!219 = !DILocation(line: 58, column: 31, scope: !220)
!220 = distinct !DILexicalBlock(scope: !215, file: !1, line: 57, column: 51)
!221 = !DILocation(line: 58, column: 36, scope: !220)
!222 = !DILocation(line: 58, column: 39, scope: !220)
!223 = !DILocation(line: 58, column: 21, scope: !220)
!224 = !DILocation(line: 58, column: 26, scope: !220)
!225 = !DILocation(line: 58, column: 29, scope: !220)
!226 = !DILocation(line: 59, column: 17, scope: !220)
!227 = !DILocation(line: 57, column: 45, scope: !215)
!228 = distinct !{!228, !217, !229, !52}
!229 = !DILocation(line: 59, column: 17, scope: !133)
!230 = !DILocation(line: 61, column: 9, scope: !126)
!231 = !DILocation(line: 61, column: 9, scope: !125)
!232 = !DILocation(line: 46, column: 33, scope: !126)
!233 = distinct !{!233, !174, !234, !52}
!234 = !DILocation(line: 61, column: 9, scope: !121)
!235 = !DILocation(line: 64, column: 38, scope: !122)
!236 = !DILocation(line: 64, column: 19, scope: !122)
!237 = !DILocation(line: 64, column: 16, scope: !122)
!238 = !DILocation(line: 65, column: 5, scope: !122)
!239 = !DILocation(line: 44, column: 47, scope: !123)
!240 = distinct !{!240, !168, !241, !52}
!241 = !DILocation(line: 65, column: 5, scope: !119)
!242 = !DILocation(line: 67, column: 10, scope: !109)
!243 = !DILocation(line: 67, column: 5, scope: !109)
!244 = !DILocation(line: 68, column: 20, scope: !109)
!245 = !DILocation(line: 68, column: 5, scope: !109)
!246 = !DILocation(line: 69, column: 5, scope: !109)
!247 = !DILocation(line: 70, column: 1, scope: !109)
